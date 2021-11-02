from django.shortcuts import render
from django.http import HttpResponse	

def auth(request):

	"""
	Authenticates the user, after authentication if the user is superuser
	go to  'super_user/super_user.html' otherwise go to 
	'normal_user/normal_user.html'
	"""

	# email_address = request.POST.get('email_address', None) 
	# password = request.POST.get('password', None)
	
	# from .models import User
	# u = User.objects.filter(email=email_address).values()

	# if not u: # if provided email is not found in User table.
	#     return render(request, 'user_not_found.html')
	# else: # if the email is found in DB.
	# 	if u[0]['password'].strip() == password:
	# 		# AUTHENTICATED
	# 		if u[0]['is_superuser']:
	# 			return render(request, 'super_user/super_user.html')
	# 		else:
	# 			return render(request, 'normal_user/normal_user.html')
	# 	else:
	# 		return render(request, 'wrong_password.html')
	return render(request, 'normal_user/normal_user.html')


	# NOTE: opar waly code ko uncomment karny k sath hi login.html templace me email and password ko required kar den
