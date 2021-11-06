from django.db import models

class country(models.Model):
	name = models.TextField(max_length=255)
	created_at = models.DateTimeField()
	class Meta:
		db_table = "country"

class Players(models.Model):
	country_id = models.IntegerField()
	name = models.TextField(max_length=255)
	category= models.TextField(max_length=255)
	class Meta:
		db_table = "Players"


class Matches(models.Model):
	country_1  = models.TextField(max_length=255)
	country_2  = models.TextField(max_length=255)
	date       = models.DateField()
	created_at = models.DateTimeField()
	recorded   = models.IntegerField(default=0)
	class Meta:
		db_table = "Matches"


class Player_score(models.Model):

	match_id = models.IntegerField()
	player_id = models.IntegerField()
	country_id = models.IntegerField()

	player_name = models.TextField(max_length=40)
	runs = models.IntegerField()
	wickets = models.IntegerField()
	catches = models.IntegerField()
	stumps = models.IntegerField()
	total = models.IntegerField()

	class Meta:
		db_table = "Player_score"