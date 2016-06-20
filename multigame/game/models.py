from django.db import models

# Create your models here.
class UserProfile(models.Model):
	userid = models.AutoField(primary_key=True)
	username = models.CharField(max_length=200)
	color = models.CharField(max_length=200)

class Game(models.Model):
	gameid = models.AutoField(primary_key=True)
	square = models.IntegerField()
	no_of_player = models.IntegerField(default = 0)
	is_active = models.BooleanField(default = False)
	is_completed = models.BooleanField(default = False)
	challenge = models.ForeignKey(UserProfile)

