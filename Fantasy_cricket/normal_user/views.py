from django.shortcuts import render
from super_user.models import *
from django.db import connection
cursor = connection.cursor()




def create_team(request):

	data = cursor.execute('''
		select c.name, p.name, p.category
		from players p
		LEFT JOIN country c
		ON c.id = p.country_id''').fetchall()

	param = {'bowler' : [],
            'all_rounder' : [],
            'wicket_keeper' : [],
            'batsman' : []}
	
	for i in data:
		param[i[-1]].append((i[1], i[0]))

	return render(request, "create_team.html", param)
