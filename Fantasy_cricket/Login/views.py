from django.shortcuts import render
from django.http import HttpResponse	
# Create your views here.

def auth(request):
	email_address = request.POST.get('email_address', None) 
	password = request.POST.get('password', None)
	
	from .models import User
	u = User.objects.filter(email=email_address).values()
	if not u:
		# User not exist
	    return render(request, 'user_not_found.html')
	else:
		# print("..................")
		# print(password)
		# print("..................")
		if u[0]['password'] == password:
			# AUTHENTICATED
			return render(request, 'normal_user/normal_user.html')

	# u = User(email="my_email", full_name="my_full_name", password="my_password")
