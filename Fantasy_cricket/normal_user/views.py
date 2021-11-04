from django.shortcuts import render
from super_user.models import *
from django.http import HttpResponse
import pandas as pd
from django.db import connection
from django.http import JsonResponse

def create_team(request):
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



def my_form(request):

	print("------------------------------------")
	print(request.user.username)
	# for i in dir(request):
	# 	x = f"request.{i}"
	# 	try:
	# 		print("----------------\n\n\n"+i+"\n")
	# 		print(eval(x))
	# 	except:
	# 		pass
	# print(request.user)
	# for k,v in dict(request.POST).items():
	# 	if k.isdigit():
	# 		name, country, type_ = v[0].split("|")
	# 		print(k, name, country, type_)
	
	print("------------------------------------")
	return HttpResponse("""<html><body><h1>HY</h1></body></html>""")


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
	wicket_keeper_select_more_task_completed = ("true" if df['type'].eq("wicket_keeper").sum() >= 2 else "false")
	left_players_task_completed              = ("true" if len(df) == 11 else "false")
	left_countries_task_completed            = ("true" if len(df.country.unique()) >= 3 else "false")
	can_submit                               = all([i == "true" for i in [betsman_select_more_task_completed, bowlers_select_more_task_completed, all_rounder_select_more_task_completed, wicket_keeper_select_more_task_completed, left_players_task_completed, left_countries_task_completed] ])
	can_submit                               = ("true" if can_submit else "false")
	can_submit = "true" # ONLY for testing, remove it immediatly, amir

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