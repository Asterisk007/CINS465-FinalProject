from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import User

def dashboard(request):
	return render("core/dashboard.html")