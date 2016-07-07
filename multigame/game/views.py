from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from game.models import *
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Max
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
	loop = int(gridsize)
	gameid = random.randint(1,1000000)
	usercolor = random.choice(color_array)
	#print(usercolor)
	game_instance = Game.objects.create(gameid = gameid ,square = gridsize , owner = username , no_of_player = 1)
	user_instance = UserProfile.objects.create(username = username ,color = usercolor , challenge = Game.objects.get(gameid=gameid))
	request.session['game_id'] = gameid
	request.session['user_color'] = usercolor
	request.session['username'] = username
	request.session['gridsize'] = gridsize	
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
    game_to_join = Game.objects.filter(is_completed = False , no_of_player__range =(1,3))
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
	#print (newfinalcol)
	request.session['game_id'] = gid
	request.session['user_color'] = newfinalcol
	request.session['username'] = playername
	request.session['gridsize'] = update_game.square
	user_instance = UserProfile.objects.create(username = playername ,color = newfinalcol , challenge = Game.objects.get(gameid=gid))
	template = loader.get_template("game/template/game/waitpage.html")
	return HttpResponse(template.render())

def buildArena(request):
	if request.is_ajax():
		grid_game_id = request.session['game_id']
		print (grid_game_id)
		game_data = Game.objects.filter(gameid = grid_game_id)
		#square = game_data.square
		game_details = serializers.serialize("json", game_data)
		data = {'game_details' : game_details}
		return JsonResponse(data)	
	else:	
		template = loader.get_template("game/template/game/arena.html")
		return HttpResponse(template.render())

def gameStatus(request):
	if request.is_ajax():
		grid_game_id = request.session['game_id']
		col = request.session['user_color']
		game_data = Game.objects.get(gameid = grid_game_id)
		status = game_data.is_active
		grid_view = GameDetails.objects.filter(gameref = Game.objects.get(gameid = grid_game_id))
		grid_details = serializers.serialize("json", grid_view)
		player_data = UserProfile.objects.filter(challenge=Game.objects.get(gameid = grid_game_id))
		player_details = serializers.serialize("json", player_data)
		playerscore = UserProfile.objects.get(challenge = Game.objects.get(gameid = grid_game_id) , color = col )
		score = playerscore.score
		gridsize = request.session['gridsize']
		data = {'status':status , 'grid_details' : grid_details , 'player_details' : player_details , 'score' : score , 'gridsize' : gridsize}
		return HttpResponse(json.dumps(data), content_type='application/json')

def changeStatus(request):
	if request.is_ajax():
		gid = request.session['game_id']
		update_status = Game.objects.get(gameid = gid)
		update_status.is_active = True
		update_status.save()
		data = {}
		return JsonResponse(data)

def updateScore(request):
	if request.is_ajax():
		divid = request.POST['id']
		gameid = request.session['game_id']
		usercol = request.session['user_color']
		divcount = GameDetails.objects.filter(divs = divid , gameref =  Game.objects.get(gameid=gameid))
		if (divcount.count() == 0):
			game_details_instance = GameDetails.objects.create(divs = divid , div_color = usercol , gameref =  Game.objects.get(gameid=gameid))
			update_status = Game.objects.get(gameid = gameid)
			update_status.is_active = False
			update_status.save()
			update_player_score = UserProfile.objects.get(challenge= Game.objects.get(gameid = gameid) , color = usercol)
			update_player_score.score += 1
			update_player_score.save()
			data = {'divid' : divid , 'usercol' : usercol}
			return JsonResponse(data)
		else:
			data = {}
			return JsonResponse(data)

def finalDisplay(request):
	if request.is_ajax():
		gid = request.session['game_id']
		col = request.session['user_color']
		update_status = Game.objects.get(gameid = gid)
		update_status.is_complete = False
		update_status.save()
		max_score = UserProfile.objects.filter(challenge= Game.objects.get(gameid = gid)).aggregate(Max('score'))['score__max']
		allwinners = UserProfile.objects.filter(challenge= Game.objects.get(gameid = gid),score = max_score)
		playerscore = UserProfile.objects.get(challenge = Game.objects.get(gameid = gid) , color = col )
		score = playerscore.score
		if (score == max_score):
			your_res = "win"
		else:
			your_res = "no"
		allwinners_details = serializers.serialize("json", allwinners)
		data = {"allwin" : allwinners_details , "your_res" : your_res}
		return JsonResponse(data)

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

