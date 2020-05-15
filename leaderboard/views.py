from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from leaderboard.models import PlayerScore, LeaderboardSerializer

# Create your views here.
@login_required(login_url="/login/")
def leaderboard(request):
	listings = PlayerScore.objects.all().order_by("-score")
	print(listings)
	data = {
		"title":"Leaderboard",
		"listings":listings
	}
	return render(request, "leaderboard/leaderboard.html", data)

class LeaderboardViewSet(viewsets.ModelViewSet):
	queryset = PlayerScore.objects.all()
	serializer_class = LeaderboardSerializer
	permission_classes = [permissions.IsAuthenticated]