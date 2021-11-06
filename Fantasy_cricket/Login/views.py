from django.shortcuts import render
from django.http import HttpResponse	
from .models import User
from django.contrib.auth import authenticate, login

def auth(request):

	"""
	Authenticates the user, after authentication if the user is superuser
	go to  'super_user/super_user.html' otherwise go to 
	'normal_user/normal_user.html'
	"""
	# request.user.username
	
	# email_address = request.POST['email_address'] 
	# password      = request.POST['password']


	# try:
	# 	user = User.objects.get(email=email_address)
	# except User.DoesNotExist:
	# 	return render(request, 'user_not_found.html', {"error" : "User not exist."})
	# if not user.check_password(password):
	# 	return render(request, 'user_not_found.html', {"error" : "Wrong email or password"})
	# if user.is_active:			
	# 	login(request, user)
	# 	if user.is_superuser:
	# 		return render(request, 'super_user/super_user.html')
	# 	else:
	# 		return render(request, 'normal_user/normal_user.html')
	# else:
	# 	return render(request, 'user_not_found.html', {"error" : "User not active"})
	return render(request, 'super_user/super_user.html')
	# NOTE: opar waly code ko uncomment karny k sath hi login.html templace me email and password ko required kar den


