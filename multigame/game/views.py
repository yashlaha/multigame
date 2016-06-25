from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from game.models import Game,UserProfile
from django.core import serializers
from django.http import JsonResponse
import random
import json
import socket


# Create your views here.
color_array = ['red','green','blue','yellow','pink','violet','aqua','brown','darkblue','darkgreen','magenta','ivory']
def index (request):
    template = loader.get_template("game/template/game/index.html")
    return HttpResponse(template.render())

def addGame(request):
	username = request.POST['player_name']
	gridsize = request.POST['grid_size']
	gameid = random.randint(1,1000000)
	usercolor = random.choice(color_array)
	print(usercolor)
	game_instance = Game.objects.create(gameid = gameid ,square = gridsize , owner = username , no_of_player = 1)
	user_instance = UserProfile.objects.create(username = username ,color = usercolor , challenge = Game.objects.get(gameid=gameid))
	request.session['game_id'] = gameid
	request.session['user_color'] = usercolor
	request.session['username'] = username	
	template = loader.get_template("game/template/game/waitpage.html")
	return HttpResponse(template.render())

def checkUser(request):
	gameid_join = request.session['game_id']
	name = request.session['username']
	gameobject = Game.objects.get(gameid = gameid_join)
	playercount = gameobject.no_of_player
	data = {'playercount':playercount , 'name' : name , 'game' : gameid_join}
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
	print (newfinalcol)
	request.session['game_id'] = gid
	request.session['user_color'] = newfinalcol
	request.session['username'] = playername
	user_instance = UserProfile.objects.create(username = playername ,color = newfinalcol , challenge = Game.objects.get(gameid=gid))
	template = loader.get_template("game/template/game/waitpage.html")
	return HttpResponse(template.render())

def buildArena(request):
	if request.is_ajax():
		grid_game_id = request.session['game_id']
		print (grid_game_id)
		game_data = Game.objects.filter(gameid = grid_game_id)
		#square = game_data.square
		player_data = UserProfile.objects.filter(challenge=Game.objects.get(gameid = grid_game_id))
		game_details = serializers.serialize("json", game_data)
		player_details = serializers.serialize("json", player_data)
		data = {'game_details' : game_details , 'player_details' : player_details}
		return JsonResponse(data)	
	else:	
		template = loader.get_template("game/template/game/arena.html")
		return HttpResponse(template.render())

def exitGame(request):
	try:
		del request.session['game_id']
		del request.session['user_color']
		del request.session['username']
	except KeyError:
		pass
	template = loader.get_template("game/template/game/index.html")
	return HttpResponse(template.render())	

def pickdiffcolor(color,gameid):
	count = 0
	gid = gameid
	newcol = color
	colordata = UserProfile.objects.filter(color = newcol , challenge = Game.objects.get(gameid = gid))
	for colors in colordata:
		if (newcol == colors.color):
			count = count + 1
	if(count > 0) :
		anothercolor = random.choice(color_array)
		pickdiffcolor(anothercolor,gid)
	else:
		return newcol

def multiply(value, arg):
    return value*arg

