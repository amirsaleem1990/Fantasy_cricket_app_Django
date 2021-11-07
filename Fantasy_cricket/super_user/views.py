from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime
from operator import itemgetter	
from .models import *
import pandas as pd

def create_new_country_func(request):
	"""
	This function is ONLY for super user, using this function he will create a new countries.
	"""

	# get values from submitted form
	country_name ,playerName_1 ,player_1 ,playerName_2 ,player_2 ,playerName_3 ,player_3 ,playerName_4 ,player_4 ,playerName_5 ,player_5 ,playerName_6 ,player_6 ,playerName_7 ,player_7 ,playerName_8 ,player_8 ,playerName_9 ,player_9 ,playerName_10 ,player_10 ,playerName_11 ,player_11 ,playerName_12 ,player_12 ,playerName_13 ,player_13 ,playerName_14 ,player_14 ,playerName_15 ,player_15 = itemgetter('country_name', 'playerName_1', 'player_1', 'playerName_2', 'player_2', 'playerName_3', 'player_3', 'playerName_4', 'player_4', 'playerName_5', 'player_5', 'playerName_6', 'player_6', 'playerName_7', 'player_7', 'playerName_8', 'player_8', 'playerName_9', 'player_9', 'playerName_10', 'player_10', 'playerName_11', 'player_11', 'playerName_12', 'player_12', 'playerName_13', 'player_13', 'playerName_14', 'player_14', 'playerName_15', 'player_15')(request.POST)

	# add a new country in 'country' table
	country(
		name = country_name,
		created_at = ':'.join(str(datetime.now()).split(":")[:2]) + ":00"
		).save()

	# add players names to 'Players' table
	for player_name, category in zip(
		[playerName_1, playerName_2, playerName_3, playerName_4, playerName_5, playerName_6, playerName_7, playerName_8, playerName_9, playerName_10, playerName_11, playerName_12, playerName_13, playerName_14, playerName_15],
		[player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8, player_9, player_10, player_11, player_12, player_13, player_14, player_15]): 
		if player_name and category:
			Players(country_id = country.objects.filter(name=country_name).values()[0]['id'],
				   name = player_name,
				   category = category
				   ).save()

	return HttpResponse("""<html>
								<body>
									<h1>Country created successfully</h1>

									<br><br>

									<a href="/Create_new_country"><button>Create a new country</button></a>
									<a href="/login"><button>Go to main page</button></a>

								</body>
						   </html>""")


def create_new_match_func(request):
	"""
	This function is ONLY for super user.
	super user can crete a new match. this function is providing an information about existing teams.
	"""
	countries = [i['name'] for i in country.objects.values()]
	form = {"Teams" : countries,
			"date" : str(datetime.now().date())}
	return render(request, 'super_user/home.html',form)

# AJAX
def load_cities(request):

	provided_date = request.GET.get('date')
	first_country = request.GET.get('country_1')

	countries_to_exclude = []
	for country_ in Matches.objects.filter(
		(Q(country_1=first_country) & Q(date=provided_date)) | # match between country 1 and country 2 on the same date
		(Q(country_2=first_country) & Q(date=provided_date))   # match between country 2 and country 1 on the same date
		).all():

		countries_to_exclude += [country_.country_1, country_.country_2]
	countries_to_exclude = list(set(countries_to_exclude)) + [first_country]

	possible_second_countries = [i['name'] for i in country.objects.values() if not i['name'] in countries_to_exclude] 

	return render(request, 'super_user/dropdown_list_options.html', {'possible_second_countries': possible_second_countries})


def match_created(request):
	
	new_match = Matches(
		country_1  = request.POST["country_1"],
		country_2  = request.POST["country_2"],
		date       = request.POST["date"],
		created_at =  ':'.join(str(datetime.now()).split(":")[:2]) + ":00"
			)
	new_match.save()

	return render(request, 'super_user/match_created.html')



def record_performance_func(request):

	data = [
		[
			f"{i['country_1']}VS{i['country_2']}{'RECORDED' if i['recorded'] else 'NOTRECORDED'}",
			f"{i['country_1']}  VS {i['country_2']} ({'recorded' if i['recorded'] else 'not recorded'})",
			i['id']
		]

			for i in Matches.objects.order_by("-date").values()
		]
	return render(request, "Record_performances.html", {"data" : data, })


def leader_board_and_record_performance(request, teams, id_):
	# print("------------------")
	match_id = id_
	country_1, x = teams.split("VS")
	recorded = False
	if x.endswith("NOTRECORDED"):
		country_2 = x.rstrip("NOTRECORDED")
	else:
		country_2 = x.rstrip("RECORDED")
		recorded = True

	# get ID of country 1 from 'country' table.
	country_1_id = country.objects.filter(name=country_1).get().id
	# get ID of country 2 from 'country' table.
	country_2_id = country.objects.filter(name=country_2).get().id

	if not recorded:

		# get 'country_1' players from 'Players' table using 'country_1_id'
		country_1_players = [(i['name'], i['category']) for i in Players.objects.filter(country_id=country_1_id).values()]
		# get 'country_2' players from 'Players' table using 'country_2_id'
		country_2_players = [(i['name'], i['category']) for i in Players.objects.filter(country_id=country_2_id).values()]

		peram = {
			"data" : {
				"country_1_name" : country_1, 
				"country_2_name" : country_2, 
				"country_1_players" : country_1_players,
				"country_2_players" : country_2_players,
					 },
			"match_id" : match_id,
				}
		return render(request, "leader_board_and_record_performance.html", peram)
	else:
		peram = {
			"data" : {"country_1_players" : [],
					  "country_2_players" : [],
					  "country_1_name" : country_1,
					  "country_2_name" : country_2}
		}
		for country_id_, country_n_players in zip([country_1_id, country_2_id], ['country_1_players', 'country_2_players']):
			match_details = Player_score.objects.filter(match_id=match_id, country_id=country_id_).values()
			for player_ in match_details:
				peram['data'][country_n_players].append(
					[player_['player_name'], player_['runs'], player_['wickets'], player_['catches'], player_['stumps'], player_['total']]
					)
		return render(request, "leader_board_show_only.html", peram)
	# return HttpResponse("HI")




def record_a_score_func(request):

	data = request.POST.dict()
	
	match_id = data['match_id']
	country_1_name = data['country_1_name']
	country_2_name = data['country_2_name']

	data = {k:(0 if not v else int(v.strip())) for k,v in data.items() if not k in ['csrfmiddlewaretoken', 'country_1_name', 'country_2_name', 'match_id']}
	players = {}
	for k,v in data.items():
		country_, field_, x = k.split("|")
		player_, player_type = eval(x)
		p = player_ + "|" + country_
		if not p in players:
			players[p] = {}
		players[p][field_] = v
	for k,v in players.items():

		player_, country_ = k.split("|")
		runs    = v['run_scored']
		wickets = (v['wickets_taken'] if 'wickets_taken' in v else 0)
		catches = v['catches']
		stumps  = (v['stumps'] if 'stumps' in v else 0)

		Player_score(
			match_id    = Matches.objects.filter(country_1 = country_1_name, country_2 = country_2_name, recorded=0)[0].id, #get().id ,
			player_id   = Players.objects.filter(name=player_ ).get().id ,
			country_id  = country.objects.filter(name=country_).get().id ,
			player_name = player_,
			runs        = runs, 
			wickets     = wickets, 
			catches     = catches, 
			stumps      = stumps,
			total       = runs + wickets + catches + stumps
			).save()


	Matches.objects.filter(id=match_id).update(recorded=1)

	return HttpResponse("record_a_score_func called")






