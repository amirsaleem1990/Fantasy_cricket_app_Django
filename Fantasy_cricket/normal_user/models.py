from django.db import models
from Login.models import User
from super_user.models import Players
class Teams(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField()
	class Meta:
		db_table = "Teams"


class Team_players(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	players = models.ForeignKey(Players, on_delete=models.CASCADE)
	class Meta:
		db_table = "Team_players"
