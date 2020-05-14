from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from leaderboard.models import PlayerScore

# Create your views here.
@login_required(login_url="/login")
def leaderboard(request):
	listings = PlayerScore.objects.all().order_by("-score")
	data = {
		"title":"Leaderboard",
		"listings":listings
	}
	return render(request, "leaderboard/leaderboard.html", data)