from django.db import models
from django.contrib.auth.models import User
from leaderboard.models import PlayerScore
from rest_framework import serializers

# The central game class, for use in listing and completing games
class Game(models.Model):
	title = models.CharField(
		max_length=100
	)
	current_round = models.IntegerField(default=1)
	max_rounds = models.IntegerField(default=1)
	# Player 1 is automatically filled when a user creates a game
	player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player1", default = None)
	# Player 2 is filled when another user (who is NOT player 1) joins this game
	player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player2", default = None, null = True)
	# Number of wins player 1 has
	player1wins = models.IntegerField()
	# Number of wins player 2 has
	player2wins = models.IntegerField()
	# Whether this game is still open.
	open = models.BooleanField()
	# Whether this game has concluded.
	finished = models.BooleanField()

MOVESET = [
	("R", "Rock"),
	("P", "Paper"),
	("S", "Scissors"),
	("U", "Undecided")
]

# To assist in completing games
class GameRound(models.Model):
	# The game this round is a part of
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	# Each player makes a move
	player1_move = models.CharField(
		max_length = 1,
		blank = False,
		default = MOVESET[3][0]
	)
	player2_move = models.CharField(
		max_length = 1,
		blank = False,
		default = MOVESET[3][0]
	)

	# Returns the current status of the round:
	'''
	0: if the player must wait for the other player
	1: if the player must make their move
	'''
	def status(self, user):
		if self.player1_move == "U" and self.player2_move == "U":
			return 1
		elif self.player1_move == "U":
			if user == self.game.player1:
				return 1
			else:
				return 0
		elif self.player2_move == "U":
			if user == self.game.player2:
				return 1
			else:
				return 0


	# Set the move for a player
	'''
	Response codes:
	0: tied game, restart
	1: winning player determined, continue
	2: winning player determined and match concluded, end game
	3: run tiebreaker
	4: standby for other player
	'''
	def set_move(self, user, move):
		# Player 1's move
		if (self.game.player1 == user and self.player1_move == "U"):
			self.player1_move = move
		# Player 2's move
		elif (self.game.player2 == user and self.player2_move == "U"):
			self.player2_move = move
		
		#print(self.player1_move)
		#print(self.player2_move)
		#print(self.game.finished)

		'''
		# Player has submitted their move, but their opponent has not.
		if (self.player1_move == "U" and user != self.game.player1):
			return 4
		elif (self.player2_move == "U" and user != self.game.player2):
			return 4
		# Player has not submitted a move yet. Let them continue.
		elif (self.player1_move == "U" and user == self.game.player1):
			return 1
		elif (self.player2_move == "U" and user == self.game.player2):
			return 1
		'''

		# Check if both players have made their moves.
		if (self.player1_move != "U" and self.player2_move != "U"):
			winning_player = 0
			if (self.player1_move == "R"):
				if (self.player2_move == "R"):
					# Tie. Go again.
					winning_player = 0
				elif (self.player2_move == "P"):
					# Paper beats rock.
					winning_player = 2
				else:
					# Rock beats scissors.
					winning_player = 1
			elif (self.player1_move == "P"):
				if (self.player2_move == "R"):
					# Rock is defeated by paper.
					winning_player = 1
				elif (self.player2_move == "P"):
					# Tie. Go again.
					winning_player = 0
				else:
					# Scissors beats paper.
					winning_player = 2
			elif (self.player1_move == "S"):
				if (self.player2_move == "R"):
					# Rock beats scissors.
					winning_player = 2
				elif (self.player2_move == "P"):
					# Paper is defeated by scissors.
					winning_player = 1
				else:
					# Tie. Go again.
					winning_player = 0
			
			if winning_player == 1:
				self.game.player1wins += 1
				self.game.save()
			elif winning_player == 2:
				self.game.player2wins += 1
				self.game.save()
			elif winning_player == 0:
				# Winning player is 0 => tie. Reset and go again.
				self.player1_move = "U"
				self.player2_move = "U"
				return 0

			# Determine whether we can close this game (for best x out of y, where x = y-1)
			if (self.game.current_round == self.game.max_rounds-1):
				# We can close a game if player 1 or 2's score is greater than the other,
				# and only one round remains.
				player1_score = self.game.player1wins
				player2_score = self.game.player2wins
				if ( (player1_score > player2_score) or (player2_score > player1_score) ):
					self.game.open = False
					self.game.finished = True
					self.game.save()
					# Save player's score.
					if (player1_score > player2_score):
						player_stat, created = PlayerScore.objects.get_or_create(user = self.game.player1)
					else:
						player_stat, created = PlayerScore.objects.get_or_create(user = self.game.player2)
					player_stat.score += 1
					player_stat.save()
					#print("Game concluded")
					return 2
				# Otherwise, run a tiebreaker round. Reset players' moves.
				else:
					self.game.current_round += 1
					self.game.save()
					self.player1_move = "U"
					self.player2_move = "U"
					return 3
			elif (self.game.current_round >= self.game.max_rounds):
				player1_score = self.game.player1wins
				player2_score = self.game.player2wins
				self.game.open = False
				self.game.finished = True
				# Save player's score.
				if (player1_score > player2_score):
					player_stat, created = PlayerScore.objects.get_or_create(user = self.game.player1)
				else:
					player_stat, created = PlayerScore.objects.get_or_create(user = self.game.player2)
				player_stat.score += 1
				player_stat.save()
				self.game.save()
				return 2
			# Only when a round has finished can we reset both players' moves.
			else:
				self.game.current_round += 1
				self.game.save()
				self.player1_move = "U"
				self.player2_move = "U"
				return 1
			
class GameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Game
		fields = '__all__'