from django.db import models

class Country(models.Model):
	name = models.TextField(max_length=255)
	created_at = models.DateTimeField()
	class Meta:
		db_table = "Country"

class Players(models.Model):
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	name = models.TextField(max_length=255)
	category= models.TextField(max_length=255)
	class Meta:
		db_table = "Players"


class Matches(models.Model):
	country_1 = models.TextField(max_length=255)
	country_2 = models.TextField(max_length=255)
	date = models.DateField()
	created_at = models.DateTimeField()
	recorded = models.IntegerField(default=0)
	class Meta:
		db_table = "Matches"


class Player_score(models.Model):

	matches = models.ForeignKey(Matches, on_delete=models.CASCADE)
	players = models.ForeignKey(Players, on_delete=models.CASCADE)
	country = models.ForeignKey(Country, on_delete=models.CASCADE)

	player_name = models.TextField(max_length=40)
	runs = models.IntegerField()
	wickets = models.IntegerField()
	catches = models.IntegerField()
	stumps = models.IntegerField()
	total = models.IntegerField()

	class Meta:
		db_table = "Player_score"