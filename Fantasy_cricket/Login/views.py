from django.shortcuts import render
from django.http import HttpResponse	
from .models import User
from django.contrib.auth import authenticate, login
from normal_user.models import *
from super_user.models import *
from functools import reduce
import operator
from django.db.models import Q

def auth(request):

	"""
	Authenticates the user, after authentication if the user is superuser
	go to  'super_user/super_user.html' otherwise go to 
	'normal_user/normal_user.html'
	"""
	
	email_address = request.POST['email_address'] 
	password = request.POST['password']


	try:
		user = User.objects.get(email=email_address)
	except User.DoesNotExist:
		return render(request, 'auth_error.html', {"error" : "User not exist."})
	if not user.check_password(password):
		return render(request, 'auth_error.html', {"error" : "Wrong email or password"})
	if user.is_active:			
		login(request, user)
		if user.is_superuser:
			return render(request, 'super_user/super_user.html')
		else:
			my_user_id = request.user.id
			teams_exist = Teams.objects.filter(user_id=my_user_id)
			peram = {
				"teams_exist"    : bool(teams_exist)
				}
			return render(request, 'normal_user/normal_user.html', peram)
	else:
		return render(request, 'auth_error.html', {"error" : "User not active"})
	

