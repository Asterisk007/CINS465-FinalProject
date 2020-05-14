"""final_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import core.views as core_views
import forum.views as forum_views
import game.views as game_views
import leaderboard.views as leaderboard_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login", core_views.rps_login),
    path("logout/", core_views.rps_logout),
    path("register", core_views.register),
    path("", core_views.dashboard),
    path("game/", game_views.open_games),
    path("game/join:<int:gameid>", game_views.open_games),
    path("game/create", game_views.create_game),
    path("game/play:<int:gameid>", game_views.play_game),
    path("game/playround:<int:gameid>", game_views.play_round),
    # This url is purely for testing purposes so that I can purge things.
    # !!!!!!!!
    #path("game/delete:<int:gameid>", game_views.delete), # <<<<<<< TODO: FIXME: Delete this! <<<<<<<<
    # !!!!!!!!
    path("forum/", forum_views.forum_boards_list, name="forum"),
    path("forum/board/<str:board>", forum_views.forum_board),
    path("forum/board/<str:board>/<int:thread_id>", forum_views.view_thread),
    path("forum/post:topic=<str:topic>", forum_views.forum_newpost),
    path("leaderboard/", leaderboard_views.leaderboard),
    #path("404", core_views.not_found, name="404")
]