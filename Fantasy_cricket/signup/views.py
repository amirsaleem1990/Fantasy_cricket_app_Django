from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from Login.models import User

def create_user(request):
	"""
	This function recieves signup request form, and create a new account if provided email
	is not exists in User table.
	"""
	email_address = request.POST.get('email_address', None) 
	full_name = request.POST.get('full_name', None)
	password = request.POST.get('password', None)
	retype_password = request.POST.get('retype_password', None)

	# Get User data for given email
	u = User.objects.filter(email=email_address).values()
	if not u: # if email not found 
		# Create a user
		User.objects.create_user(full_name=full_name, email=email_address, password=password, username=full_name).save()
		return render(request, 'user_created.html')
	else: # if email already exists in User table.
		return render(request, 'email_already_in_use.html')