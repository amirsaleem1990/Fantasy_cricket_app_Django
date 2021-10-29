from django.db import models

class Players(models.Model):
	country_id = models.IntegerField()
	name = models.TextField(max_length=255)
	category= models.TextField(max_length=255)
	class Meta:
		db_table = "Players"

class country(models.Model):
	name = models.TextField(max_length=255)
	created_at = models.DateTimeField()
	class Meta:
		db_table = "country"