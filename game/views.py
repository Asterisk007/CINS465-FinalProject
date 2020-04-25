from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import User

# Main game view
@login_required(login_url="/login/")
def game(request):
	return render("game/game.html")