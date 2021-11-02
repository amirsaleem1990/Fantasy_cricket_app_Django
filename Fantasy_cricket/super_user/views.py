from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from operator import itemgetter	
from .models import country, Players, Matches
from datetime import datetime
from django.db.models import Q

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


# def create_new_match_func(request):
	"""
	This function is ONLY for super user.
	super user can crete a new match. this function is providing an information about existing teams.
	"""
	
	# from .models import country
	# teams = [i['name'] for i in country.objects.values()]
	# return render(request, "Create_matches.html", {"Teams" : teams, "date" : str(datetime.now().date())})

def create_new_match_func(request):
	# form = {"date" : ':'.join(str(datetime.now()).split(":")[:2]) + ":00",
			# "Teams" : ['team_1', 'team_2', 'team_3'], 
			# }
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