from django.db import models

class Teams(models.Model):

	user_id = models.IntegerField()
	created_at = models.DateTimeField()
	class Meta:
		db_table = "Teams"

class Team_players(models.Model):
	player_id_in_original_table = models.IntegerField()
	user_id = models.IntegerField()
	class Meta:
		db_table = "Team_players"
