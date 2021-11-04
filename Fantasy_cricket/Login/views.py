from django.shortcuts import render
from django.http import HttpResponse	
from .models import User
from django.contrib.auth import authenticate, login

def authenticate_user(email, password):
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		return (None, "User not exist.")
	if user.check_password(password):
		return (True, user)
	else:
		return (None, "Wrong email or password")

def auth(request):

	"""
	Authenticates the user, after authentication if the user is superuser
	go to  'super_user/super_user.html' otherwise go to 
	'normal_user/normal_user.html'
	"""
	# request.user.username
	
	# email_address = request.POST['email_address'] 
	# password      = request.POST['password']

	# user = authenticate_user(email_address, password)
	# if user[0] is None:
	# 	error = user[1]
	# 	return render(request, 'user_not_found.html', {"error" : error})
	# else:
	# 	user = user[1]
	# 	if user.is_active:			
	# 		login(request, user)
	# 		if user.is_superuser:
	# 			return render(request, 'super_user/super_user.html')
	# 		else:
	# 			return render(request, 'normal_user/normal_user.html')
	# 	else:
	# 		return render(request, 'user_not_found.html', {"error" : "User not found"})
	return render(request, 'super_user/super_user.html')
	# NOTE: opar waly code ko uncomment karny k sath hi login.html templace me email and password ko required kar den


