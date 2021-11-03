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
	# print("------------------------------------")
	# for k,v in dict(request.POST).items():
		# if k.isdigit():
			# name, country, type_ = v[0].split("|")
			# print(k, name, country, type_)
	# print("------------------------------------")
	return HttpResponse("""<html><body><h1>HY</h1></body></html>""")


def ajax_creation_form(request):
	print("------------------------------------")
	lst = []
	for k,v in dict(request.GET).items():
		if k.isdigit():
			lst.append([k] + v[0].split("|"))
	df = pd.DataFrame(lst, columns=['id', 'player', 'country', 'type'])
	print(df.to_string())
	print("------------------------------------")
	import json
	return JsonResponse({
						 "selected_players"          : str(len(df)                                 ),
		                 "left_players"              : str(11 - len(df)                            ),
		                 "betsman_select_more"       : str(3 - df['type'].eq("batsman").sum()      ),
						 "bowlers_select_more"       : str(3 - df['type'].eq("bowler").sum()       ),
						 "all_rounder_select_more"   : str(2 - df['type'].eq("all_rounder").sum()  ),
						 "wicket_keeper_select_more" : str(1 - df['type'].eq("wicket_keeper").sum()),
		                 })
	# return HttpResponse("""<html><body><h1>HY</h1></body></html>""")