from django.shortcuts import render
from django.http import HttpResponse	
from .models import User
from django.contrib.auth import authenticate, login
from normal_user.models import *

def auth(request):

	"""
	Authenticates the user, after authentication if the user is superuser
	go to  'super_user/super_user.html' otherwise go to 
	'normal_user/normal_user.html'
	"""
	
	email_address = request.POST['email_address'] 
	password      = request.POST['password']


	try:
		user = User.objects.get(email=email_address)
	except User.DoesNotExist:
		return render(request, 'user_not_found.html', {"error" : "User not exist."})
	if not user.check_password(password):
		return render(request, 'user_not_found.html', {"error" : "Wrong email or password"})
	if user.is_active:			
		login(request, user)
		if user.is_superuser:
			return render(request, 'super_user/super_user.html')
		else:
			teams_exist = bool(Teams.objects.filter(user_id=request.user.id))
			return render(request, 'normal_user/normal_user.html', {"teams_exist" : teams_exist})
	else:
		return render(request, 'user_not_found.html', {"error" : "User not active"})


