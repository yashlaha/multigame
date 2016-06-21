from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from game.models import Game,UserProfile
import random


# Create your views here.
def index (request):
    template = loader.get_template("game/template/index.html")
    return HttpResponse(template.render())

def addGame(request):
	username = request.POST['player_name']
	gridsize = request.POST['grid_size']
	usercolor = request.POST['color']
	gameid = random.randint(1,1000000)
	game_instance = Game.objects.create(gameid = gameid ,square = gridsize , no_of_player = 1)
	game_instance.save()
	user_instance = UserProfile.objects.create(username = username ,color = usercolor , challenge = Game.objects.get(gameid=gameid))
	user_instance.save()
	request.session['game_id'] = gameid
	request.session['user_color'] = usercolor
	request.session['username'] = username	
	template = loader.get_template("game/template/waitpage.html")
	return HttpResponse(template.render())