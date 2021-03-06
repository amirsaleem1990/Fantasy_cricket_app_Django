
# from django.core import paginator
from django.core.paginator import Paginator
from django.contrib.auth.decorators import *
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from super_user.models import Country, Players, Matches, Player_score
import pandas as pd
import operator
from datetime import datetime
from Login.models import User
from .models import Teams, Team_players
from functools import reduce

def check_normal_user(user):
   return not user.is_superuser



@user_passes_test(check_normal_user)
def create_team(request):
	if Teams.objects.filter(user_id=request.user.id):
		return HttpResponse("You team is already created!")
	cursor = connection.cursor()

	data = cursor.execute('''
		select c.name, p.name, p.category
		from players p
		LEFT JOIN country c
		ON c.id = p.country_id''').fetchall()
	# [('pakistan', 'p_1', 'batsman'), ('pakistan', 'p_2', 'bowler'), ('pakistan', 'p_3', 'all_rounder'), ('pakistan', 'p_4', 'wicket_keeper'), ('pakistan', 'p_5', 'batsman'), ('pakistan', 'p_6', 'batsman'), ('pakistan', 'p_7', 'batsman'), ('pakistan', 'p_8', 'batsman'), ('pakistan', 'p_9', 'batsman'), ('pakistan', 'p_10', 'batsman'), ('pakistan', 'p_11', 'batsman')]

	count_by_type = {}
	countries_qty = len(set([i[0] for i in data]))
	for i in data:
		count_by_type[i[2]] = count_by_type.get(i[2], 0) + 1
	if not data or (count_by_type['bowler'] < 3)  or (count_by_type['batsman'] < 3) or (count_by_type['all_rounder'] < 2) or (countries_qty < 3):
		return HttpResponse("Sorry, There is no team to build your team from. please try later.")
	param = {'bowler' : [],
			'all_rounder' : [],
			'wicket_keeper' : [],
			'batsman' : []}
	
	for e,i in enumerate(data):
		param[i[-1]].append((i[1], i[0], e))
	return render(request, "create_team.html", param)


@user_passes_test(check_normal_user)
def my_form(request):

	for k,v in dict(request.POST).items():
		if k.isdigit():
			name, country_, type_ = v[0].split("|")
			country_id = Country.objects.filter(name=country_).get().id
			Team_players(
				players_id = Players.objects.filter(name=name, country_id=country_id).get().id,
				user_id = request.user.id
				).save()

	Teams(
		user_id=request.user.id, 
		created_at=':'.join(str(datetime.now()).split(":")[:2]) + ":00"
		).save()
	return HttpResponse("""
	<html>
	<body>
		<h1>Your team creates successfully</h1>
		<a href="http://127.0.0.1:8000/login">Go to main page</a>
	</body>
	</html>
	""")


@user_passes_test(check_normal_user)
def ajax_creation_form(request):
	lst = []
	for k,v in dict(request.GET).items():
		if k.isdigit():
			lst.append([k] + v[0].split("|"))
	df = pd.DataFrame(lst, columns=['id', 'player', 'country', 'type'])

	betsman_select_more_task_completed = ("true" if df['type'].eq("batsman").sum() >= 3 else "false")
	bowlers_select_more_task_completed = ("true" if df['type'].eq("bowler").sum() >= 3 else "false")
	all_rounder_select_more_task_completed = ("true" if df['type'].eq("all_rounder").sum() >= 2 else "false")
	wicket_keeper_select_more_task_completed = ("true" if df['type'].eq("wicket_keeper").sum() >= 1 else "false")
	left_players_task_completed = ("true" if len(df) == 11 else "false")
	left_countries_task_completed = ("true" if len(df.country.unique()) >= 3 else "false")
	can_submit = all([i == "true" for i in [betsman_select_more_task_completed, bowlers_select_more_task_completed, all_rounder_select_more_task_completed, wicket_keeper_select_more_task_completed, left_players_task_completed, left_countries_task_completed] ])
	can_submit = ("true" if can_submit else "false")
	# can_submit = "true"
	return JsonResponse({
						 "selected_players" : str(len(df)),
						 "betsman_select_more" : str(3 - df['type'].eq("batsman").sum()),
						 "left_players" : str(11 - len(df)),
						 "bowlers_select_more" : str(3 - df['type'].eq("bowler").sum()),
						 "all_rounder_select_more" : str(2 - df['type'].eq("all_rounder").sum()),
						 "wicket_keeper_select_more" : str(1 - df['type'].eq("wicket_keeper").sum()),
						 "all_players_selected" : ("true" if len(df) == 11 else "false"),
						 "left_countries" : str(3 - len(df.country.unique())),
						 "ids_do_not_desable" : df.apply(lambda x:x.player+"|"+x.country, axis=1).to_list(),

						 "betsman_select_more_task_completed" : betsman_select_more_task_completed ,
						 "bowlers_select_more_task_completed" : bowlers_select_more_task_completed ,
						 "all_rounder_select_more_task_completed" : all_rounder_select_more_task_completed ,
						 "wicket_keeper_select_more_task_completed" : wicket_keeper_select_more_task_completed ,
						 "left_players_task_completed" : left_players_task_completed ,
						 "left_countries_task_completed" : left_countries_task_completed ,
						 "can_submit" : can_submit,
						 })


def get_user_team_score(user_id):
	team_obj = Teams.objects.filter(user_id=user_id)
	if not bool(team_obj):
		return "You're not created you team yet, Please create your team first"
	team_created_at = team_obj.get().created_at
	matches_to_consider_ids = [i['id'] for i in Matches.objects.filter(created_at__gte=team_created_at, recorded=1).values()]
	# print("..................2", user_id)
	players_ids = [i['players_id'] for i in Team_players.objects.filter(user_id=user_id).values()]
	# print(players_ids)
	# print("................................ 3")
	players = Player_score.objects.filter(reduce(operator.or_, (Q(players_id=x) for x in players_ids))).values()
	if not players:
		return "Sorry, this page is not availible."
	lst = []
	for i in players:
		if i['matches_id'] in matches_to_consider_ids:
				lst.append(i)
	if not lst:
			return "Sorry, this page is not availible #1"
	df = pd.DataFrame(lst).groupby('players_id').sum().loc[:, "runs" : "total"].reset_index()
	df['name'] = df.players_id.apply(lambda x:Players.objects.filter(id=x).get().name)
	return df

@user_passes_test(check_normal_user)
def team_performance(request):
	my_user_id = request.user.id
	df = get_user_team_score(my_user_id)
	if isinstance(df, str):
		return HttpResponse(df)
	# df
	#   players_id  runs  wickets  catches  stumps  total  name
	# 0        196    20        1        5       0     26   p_2
	# 1        197     4        9        2       0     15   p_3
	# 2        199     8        7        8       0     23   p_5
	# 3        200     7        9        2       0     18   p_6
	# 4        201     3        4        8       0     15   p_7
	# 5        207     1        1        3       0      5  p_12
	# 6        208     1        5        8       0     14  p_13
	# 7        209    12        0        3       4     19  p_14
	total = df.total.sum()
	data = df.apply(pd.Series.to_list, axis=1).to_list()
	# [[196, 20, 1, 5, 0, 26, 'p_2'],
	#  [197, 4, 9, 2, 0, 15, 'p_3'],
	#  [199, 8, 7, 8, 0, 23, 'p_5'],
	#  [200, 7, 9, 2, 0, 18, 'p_6'],
	#  [201, 3, 4, 8, 0, 15, 'p_7'],
	#  [207, 1, 1, 3, 0, 5, 'p_12'],
	#  [208, 1, 5, 8, 0, 14, 'p_13'],
	#  [209, 12, 0, 3, 4, 19, 'p_14']]
	return render(request, "team_performance.html", {"data" : data, 'total' : total})




@user_passes_test(check_normal_user)
def leader_board(request):
	users_ids = [i['user_id'] for i in Teams.objects.values()]

	my_user_id = request.user.id
	
	data = {}
	for user_id in users_ids:
		x = get_user_team_score(user_id)
		if user_id == my_user_id and (isinstance(x, str)):
			return HttpResponse("Sorry, this page is not availible #1")
		if not isinstance(x, str):
    			data[user_id] = x.total.sum()
	if not data:
		return HttpResponse("Sorry, this page is not availible #1")
	print("------------------------")
	print(data)
	data = list(enumerate(sorted(data.items(), key=lambda x:x[1], reverse=True), start=1))       
	 # [
	 # (9, (4, 8)),
	 # (8, (6, 7)),
	 # (7, (1, 5)),
	 # (6, (5, 5)),
	 # (5, (8, 4)),
	 # (4, (3, 3)),
	 # (3, (2, 3)),
	 # (2, (0, 2)),
	 # (1, (7, 2)),
	 # (0, (9, 0))
	 # ]

	my_data = [i for i in data if i[1][0] == my_user_id][0]

	# https://www.youtube.com/watch?v=Z1A0TdZzDkE
	paginator = Paginator(data, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	peram = {
				"data" : page_obj,
				"total_score" : data, 
				"your_score" : my_data[1][1],
				"your_position" : my_data[0]
				}

	return render(request, "leader_board.html", peram)