from django.db import models

class country(models.Model):
	name = models.TextField(max_length=255)
	created_at = models.DateTimeField()
	class Meta:
		db_table = "country"

class Players(models.Model):
	# country_id = models.ForeignKey('country', on_delete=models.CASCADE, db_constraint=False)
	# country_id = models.ForeignKey(country, on_delete=models.CASCADE)
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
	class Meta:
		db_table = "Matches"