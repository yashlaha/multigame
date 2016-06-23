from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from game.models import Game,UserProfile
import random
import json


# Create your views here.
color_array = ['red','green','blue','yellow','pink','violet','black']
def index (request):
    template = loader.get_template("game/template/game/index.html")
    return HttpResponse(template.render())

def addGame(request):
	username = request.POST['player_name']
	gridsize = request.POST['grid_size']
	gameid = random.randint(1,1000000)
	usercolor = random.choice(color_array)
	game_instance = Game.objects.create(gameid = gameid ,square = gridsize , owner = username , no_of_player = 1)
	user_instance = UserProfile.objects.create(username = username ,color = usercolor , challenge = Game.objects.get(gameid=gameid))
	request.session['game_id'] = gameid
	request.session['user_color'] = usercolor
	request.session['username'] = username	
	template = loader.get_template("game/template/game/waitpage.html")
	return HttpResponse(template.render())

def checkUser(request):
	gameid_join = request.session['game_id']
	gameobject = Game.objects.get(gameid = gameid_join)
	playercount = gameobject.no_of_player
	data = {'playercount':playercount}
	return HttpResponse(json.dumps(data), content_type='application/json')

def userJoin(request):
    template = loader.get_template("game/template/game/joingame.html")
    game_to_join = Game.objects.filter(is_completed = False)
    data = {'game_to_join':game_to_join}
    return HttpResponse(template.render(data,request))

def existJoin(request):
	playername = request.POST['newuser']
	gid = request.POST['gid']
	update_game = Game.objects.get(gameid = gid)
	update_game.no_of_player += 1
	update_game.save()
	newusercol = random.choice(color_array)
	newfinalcol = pickdiffcolor(newusercol,gid)
	request.session['game_id'] = gid
	request.session['user_color'] = newfinalcol
	request.session['username'] = playername
	user_instance = UserProfile.objects.create(username = playername ,color = newfinalcol , challenge = Game.objects.get(gameid=gid))
	template = loader.get_template("game/template/game/waitpage.html")
	return HttpResponse(template.render())

def pickdiffcolor(color,gameid):
	gid = gameid
	newcol = color
	if UserProfile.objects.filter(color = color , challenge = Game.objects.get(gameid=gameid)):
		newcol = random.choice(color_array)
		pickdiffcolor(newcol,gameid)
	else:
		return newcol 

