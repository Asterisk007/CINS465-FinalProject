from django import forms
from game.models import Game, MOVESET

class CreateGameForm(forms.Form):
	gametitle = forms.CharField(
		label = "Game title",
		widget=forms.TextInput(
			attrs={
				"class":"form-control"
			}
		),
		min_length=1
	)
	max_rounds = forms.IntegerField(
		label = "Number of rounds to play:",
		widget=forms.NumberInput(
			attrs={
				"class":"form-control"
			}
		),
		min_value=3,
		max_value=10
	)

	def save(self, user):
		newgame = Game(
			title = self.cleaned_data["gametitle"],
			current_round = 1,
			max_rounds = self.cleaned_data["max_rounds"],
			player1 = user,
			open = True,
			finished = False,
			player1wins = 0,
			player2wins = 0
		)
		newgame.save()

class SelectMoveForm(forms.Form):
	option = forms.ChoiceField(
		widget=forms.RadioSelect(),
		choices=MOVESET
	)