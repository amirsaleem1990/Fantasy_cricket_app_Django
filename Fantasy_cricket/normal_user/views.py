from django.shortcuts import render
from super_user.models import *
from django.http import HttpResponse


def create_team(request):
	print("_---------------------------------!!!!")
	from django.db import connection
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
	for k,v in dict(request.POST).items():
		if k.isdigit():
			name, country, type_ = v[0].split("|")
			print(k, name, country, type_)
	print("------------------------------------")
	return HttpResponse("""<html><body><h1>HY</h1></body></html>""")