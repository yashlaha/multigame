"""multigame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^startgame/', views.addGame,name='startGame'),
    url(r'^userjoin/', views.checkUser,name='checkUser'),
    url(r'^joingame/', views.userJoin,name='userJoin'),
    url(r'^joinexistgame/', views.existJoin,name='existJoin'),
    url(r'^arena/', views.buildArena,name='buildArena'),
    url(r'^checkgamestatus/', views.gameStatus,name='gameStatus'),
    url(r'^changegamestatus/', views.changeStatus,name='changeStatus'),
    url(r'^updatescore/', views.updateScore,name='updateScore'),
    url(r'^exit/', views.exitGame,name='exitGame'),
]
