from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from game.models import Game, GameRound

from core.forms import JoinForm, LoginForm

@login_required(login_url='/login')
def dashboard(request):
	make_move = []
	for item in Game.objects.filter(player1 = request.user, finished = False):
		if GameRound.objects.filter(game = item).count() == 1:
			if GameRound.objects.get(game = item).status(request.user) == 1:
				make_move.append(item)
	for item in Game.objects.filter(player2 = request.user, finished = False):
		if GameRound.objects.filter(game = item).count() == 1:
			if GameRound.objects.get(game = item).status(request.user) == 1:
				make_move.append(item)

	wait_for_player = []
	for item in Game.objects.filter(player1 = request.user, finished = False):
		if GameRound.objects.filter(game = item).count() == 1:
			if GameRound.objects.get(game = item).status(request.user) == 0:
				wait_for_player.append(item)
	for item in Game.objects.filter(player2 = request.user, finished = False):
		if GameRound.objects.filter(game = item).count() == 1:
			if GameRound.objects.get(game = item).status(request.user) == 0:
				wait_for_player.append(item)
	for item in Game.objects.filter(player1 = request.user, open = True):
		wait_for_player.append(item)

	concluded_games = []
	for item in Game.objects.filter(player1 = request.user, finished = True):
		concluded_games.append(item)
	for item in Game.objects.filter(player2 = request.user, finished = True):
		concluded_games.append(item)
	
	data = {
		"title":"User dashboard",
		"make_move":make_move,
		"wait_for_player":wait_for_player,
		"concluded_games":concluded_games,
		"cur_user":request.user
	}
	return render(request, "core/dashboard.html", data)

def rps_login(request):
	if request.method=="POST":
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if (user):
				if (user.is_active):
					login(request, user)
					return redirect("/")
				else:
					return HttpResponse("Your account is not currently active.")
			else: #User not found. They'll have to sign up.
				print("Login failed. User \"{0}\" does not exist in the system, or you used the wrong password.".format(username))
				return render(request, 'core/login.html', {"title":"User login", "login_form":LoginForm})
	else:
		return render(request, "core/login.html", {"title":"User login", "login_form":LoginForm})

@login_required(login_url="/login/")
def rps_logout(request):
    logout(request)
    return redirect("/")

def register(request):
	if request.method=="POST":
		join_form = JoinForm(request.POST)
		if (join_form.is_valid()):
			user = join_form.save()
			user.set_password(user.password)
			user.save()
			return redirect("/")
		else:
			print(join_form.errors)
	else:
		return render(request, "core/register.html", {"title":"Register", "join_form": JoinForm()})

def not_found(request):
	return render(request, "core/404.html")