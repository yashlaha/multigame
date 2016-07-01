from django.db import models

# Create your models here.
class Game(models.Model):
	gameid = models.IntegerField()
	square = models.IntegerField()
	owner = models.CharField(max_length=100)
	no_of_player = models.IntegerField(default = 0)
	is_active = models.BooleanField(default = False)
	is_completed = models.BooleanField(default = False)
	

class UserProfile(models.Model):
	userid = models.AutoField(primary_key=True)
	username = models.CharField(max_length=200)
	color = models.CharField(max_length=200)
	score = models.IntegerField(default = 0)
	challenge = models.ForeignKey(Game)

class GameDetails(models.Model):
	divs = models.CharField(max_length=100)
	div_color = models.CharField(max_length=100 , default = "black")
	gameref = models.ForeignKey(Game)