from django.shortcuts import render
from super_user.models import *
from django.http import HttpResponse
import pandas as pd
from django.db import connection
from django.http import JsonResponse
from datetime import datetime
from .models import *
from Login.models import User
from django.contrib.auth.decorators import *
from functools import reduce
import operator
from django.db.models import Q


def check_normal_user(user):
   return not user.is_superuser


@user_passes_test(check_normal_user)
def create_team(request):
	# print("====================================")
	# print(request.user.id)
	# print("====================================")
	if Teams.objects.filter(user_id=request.user.id):
		return HttpResponse("You team is already created!")
	cursor = connection.cursor()

	data = cursor.execute('''
		select c.name, p.name, p.category
		from players p
		LEFT JOIN country c
		ON c.id = p.country_id''').fetchall()

	param = {'bowler' : [],
            'all_rounder' : [],
            'wicket_keeper' : [],
            'batsman' : []}
	
	for e,i in enumerate(data):
		param[i[-1]].append((i[1], i[0], e))
	return render(request, "create_team.html", param)


@user_passes_test(check_normal_user)
def my_form(request):

	# print("------------------------------------")
	for k,v in dict(request.POST).items():
		if k.isdigit():
			name, country_, type_ = v[0].split("|")
			country_id = country.objects.filter(name=country_).get().id
			Team_players(
				player_id_in_original_table = Players.objects.filter(name=name, country_id=country_id).values()[0]['id'],
				user_id = request.user.id
				).save()

	Teams(
		user_id=request.user.id, 
		created_at=':'.join(str(datetime.now()).split(":")[:2]) + ":00"
		).save()
	return HttpResponse("""<html><body><h1>Your team creates successfully</h1></body></html>""")


@user_passes_test(check_normal_user)
def ajax_creation_form(request):
	# print("------------------------------------")
	lst = []
	for k,v in dict(request.GET).items():
		if k.isdigit():
			lst.append([k] + v[0].split("|"))
	df = pd.DataFrame(lst, columns=['id', 'player', 'country', 'type'])
	# print(df.to_string())
	# print("------------------------------------")


	betsman_select_more_task_completed       = ("true" if df['type'].eq("batsman").sum()       >= 3 else "false")
	bowlers_select_more_task_completed       = ("true" if df['type'].eq("bowler").sum()        >= 3 else "false")
	all_rounder_select_more_task_completed   = ("true" if df['type'].eq("all_rounder").sum()   >= 2 else "false")
	wicket_keeper_select_more_task_completed = ("true" if df['type'].eq("wicket_keeper").sum() >= 1 else "false")
	left_players_task_completed              = ("true" if len(df) == 11 else "false")
	left_countries_task_completed            = ("true" if len(df.country.unique()) >= 3 else "false")
	can_submit                               = all([i == "true" for i in [betsman_select_more_task_completed, bowlers_select_more_task_completed, all_rounder_select_more_task_completed, wicket_keeper_select_more_task_completed, left_players_task_completed, left_countries_task_completed] ])
	can_submit                               = ("true" if can_submit else "false")
	# can_submit = "true"
	return JsonResponse({
						 "selected_players"          : str(len(df)                                 ),
		             "left_players"              : str(11 - len(df)                            ),
		             "betsman_select_more"       : str(3 - df['type'].eq("batsman").sum()      ),
						 "bowlers_select_more"       : str(3 - df['type'].eq("bowler").sum()       ),
						 "all_rounder_select_more"   : str(2 - df['type'].eq("all_rounder").sum()  ),
						 "wicket_keeper_select_more" : str(1 - df['type'].eq("wicket_keeper").sum()),
						 "all_players_selected"      : ("true" if len(df) == 11 else "false")       ,
						 "left_countries"            : str(3 - len(df.country.unique()))            ,
						 "ids_do_not_desable"        : df.apply(lambda x:x.player+"|"+x.country, axis=1).to_list(),

						 "betsman_select_more_task_completed"      : betsman_select_more_task_completed ,
						 "bowlers_select_more_task_completed"      : bowlers_select_more_task_completed ,
						 "all_rounder_select_more_task_completed"  : all_rounder_select_more_task_completed ,
						 "wicket_keeper_select_more_task_completed": wicket_keeper_select_more_task_completed ,
						 "left_players_task_completed"             : left_players_task_completed ,
						 "left_countries_task_completed"           : left_countries_task_completed ,
						 "can_submit"                              : can_submit,
		                 })


@user_passes_test(check_normal_user)
def team_performance(request):
	
	user_id = request.user.id
	team_created_at = Teams.objects.filter(user_id=user_id).get().created_at
	matches_to_consider_ids = [i['id'] for i in Matches.objects.filter(created_at__lte=team_created_at, recorded=1).values()]

	players_ids = [i['player_id_in_original_table'] for i in Team_players.objects.filter(user_id=user_id).values()]
	players = Player_score.objects.filter(reduce(operator.or_, (Q(player_id=x) for x in players_ids))).values()
	
	lst = []
	for i in players:
		if i['match_id'] in matches_to_consider_ids:
			lst.append(i)
	df = pd.DataFrame(lst).groupby('player_id').sum().loc[:, "runs" : "total"].reset_index()
	df['name'] = df.player_id.apply(lambda x:Players.objects.filter(id=x).get().name)
	total = df.total.sum()
	#    player_id  runs  wickets  catches  stumps  total  name
	# 0        196    20        1        5       0     26   p_2
	# 1        197     4        9        2       0     15   p_3
	# 2        199     8        7        8       0     23   p_5
	# 3        200     7        9        2       0     18   p_6
	# 4        201     3        4        8       0     15   p_7
	# 5        207     1        1        3       0      5  p_12
	# 6        208     1        5        8       0     14  p_13
	# 7        209    12        0        3       4     19  p_14
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
	return render(request, "leader_board.html")