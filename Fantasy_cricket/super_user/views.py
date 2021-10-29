from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def create_new_country_func(request):
	from operator import itemgetter	
	from .models import country, Players

	country_name ,playerName_1 ,player_1 ,playerName_2 ,player_2 ,playerName_3 ,player_3 ,playerName_4 ,player_4 ,playerName_5 ,player_5 ,playerName_6 ,player_6 ,playerName_7 ,player_7 ,playerName_8 ,player_8 ,playerName_9 ,player_9 ,playerName_10 ,player_10 ,playerName_11 ,player_11 ,playerName_12 ,player_12 ,playerName_13 ,player_13 ,playerName_14 ,player_14 ,playerName_15 ,player_15 = itemgetter('country_name', 'playerName_1', 'player_1', 'playerName_2', 'player_2', 'playerName_3', 'player_3', 'playerName_4', 'player_4', 'playerName_5', 'player_5', 'playerName_6', 'player_6', 'playerName_7', 'player_7', 'playerName_8', 'player_8', 'playerName_9', 'player_9', 'playerName_10', 'player_10', 'playerName_11', 'player_11', 'playerName_12', 'player_12', 'playerName_13', 'player_13', 'playerName_14', 'player_14', 'playerName_15', 'player_15')(request.POST)

	country(
		name = country_name,
		created_at = ':'.join(str(datetime.now()).split(":")[:2]) + ":00"
		).save()

	for player_name, category in zip(
		[playerName_1, playerName_2, playerName_3, playerName_4, playerName_5, playerName_6, playerName_7, playerName_8, playerName_9, playerName_10, playerName_11, playerName_12, playerName_13, playerName_14, playerName_15],
		[player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8, player_9, player_10, player_11, player_12, player_13, player_14, player_15]): 
		if player_name and category:
			Players(country_id = country.objects.filter(name=country_name).values()[0]['id'],
				   name = player_name,
				   category = category
				   ).save()

	return HttpResponse("""<html><body><h1>Country created successfully</h1><a href="login">Go to Main Window</a>""")