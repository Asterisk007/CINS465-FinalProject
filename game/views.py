from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from game.models import Game, GameRound, MOVESET, GameSerializer
from game.forms import CreateGameForm, SelectMoveForm
from rest_framework import viewsets, permissions

# Available games to play
@login_required(login_url="/login/")
def open_games(request, gameid=None):
	# Find open games
	open_games = Game.objects.filter(open=True)
	data = {
		"title":"Open games",
		"open_games": open_games,
		"first_active":True,
		"second_active":False,
		"cur_user":request.user
	}
	return render(request, "game/opengames.html", data)

@login_required(login_url="/login/")
def create_game(request):
	if request.method == "POST":
		submission = CreateGameForm(request.POST)
		if submission.is_valid():
			submission.save(request.user)
			return redirect("/game/")

	form = CreateGameForm(initial={"max_rounds":3})
	data = {
		"title":"Create New Game",
		"first_active":False,
		"second_active":True,
		"form":form
	}
	return render(request, "game/creategame.html", data)

# Add player 2 to a created game.
@login_required(login_url="/login/")
def play_game(request, gameid=None):
	if gameid is not None:
		game = Game.objects.filter(id=gameid)
		# There should only be one game by this id. If not, something's gone wrong
		if game.count() == 1:
			cur_game = Game.objects.get(id=gameid)
			if cur_game.open == True:
				# Check that the user who wants to play is not the host (playing against yourself is impossible!)
				if cur_game.player1 != request.user:
					# Add user to this game
					cur_game.player2 = request.user
					cur_game.open = False
					cur_game.save()
					return redirect("/game/playround:{}".format(gameid))
				else:
					return redirect("/game/")
			else:
				if (cur_game.player1 == request.user) or (cur_game.player2 == request.user):
					return redirect("/game/playround:{}".format(gameid))
				else:
					return render(request, "game/closed.html")
		elif game.count() > 1 or game.count() == 0:
			# User should not be here. Either there are multiple games with this id (which probably won't happen, 
			# but I'm doing it for redundancy), or no games exist at all. Either way, tell the user it doesn't exist.
			return render(request, "game/doesnotexist.html")
		elif game.values()[0]["open"] == False:
			# User is trying to access a game that has already closed.
			return render(request, "game/closed.html")

# Carry out a game between two players
@login_required(login_url="/login/")
def play_round(request, gameid):
	# Check that this game exists.
	if Game.objects.filter(id = gameid).count() == 0:
		return render(request, "game/doesnotexist.html")

	# First get the game these players will be/have been playing
	cur_game = Game.objects.get(id=gameid)
	# Check that the game is not closed
	if cur_game.finished == False:
		response_code = -1
		# Player has made a move
		if request.method == "POST":
			#print("POST")
			# Get the round object
			cur_round = GameRound.objects.get(game = cur_game)
			player_move = SelectMoveForm(request.POST)
			# Set the move for the current user
			if player_move.is_valid():
				response_code = cur_round.set_move(request.user, player_move.cleaned_data["option"])
				cur_round.save()
			else:
				print(player_move.errors)
			
			# Once user has submitted a move, redirect them to their dashboard.
			return redirect("/")
			
		if GameRound.objects.filter(game = cur_game).count() == 0:
			# Fresh start (no rounds played)
			# Create a GameRound, which will be used to process
			# each round in this game.
			cur_round = GameRound(game = cur_game)
			cur_round.save()
		# Redirect player to make their move
		data = {
			"title":"Round {}".format(cur_game.current_round),
			"cur_game":cur_game,
			"cur_user":request.user,
			"form":SelectMoveForm()
		}
		return render(request, "game/play.html", data)
	else:
		return render(request, "game/closed.html")

'''
# Only for testing.
# FIXME: Delete this or comment it out after development!
def delete(request, gameid=None):
	game = Game.objects.filter(id=gameid)
	if game.count() > 0:
		game.delete()
	return redirect("/game/")
'''

class GameViewSet(viewsets.ModelViewSet):
	queryset = Game.objects.all()
	serializer_class = GameSerializer
	permission_classes = [permissions.IsAuthenticated]