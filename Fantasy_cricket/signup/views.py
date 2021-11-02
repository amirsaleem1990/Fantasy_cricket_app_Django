from django.shortcuts import render
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

	# if password != retype_password:
		# ???

	# Get data User table for given email
	u = User.objects.filter(email=email_address).values()
	if not u: # if email not found 
		# Create a user
		u = User(email=email_address, 
				 full_name=full_name, 
				 password=password
				 )
		u.save()
		return render(request, 'user_created.html')
	else: # if email already exists in User table.
		return render(request, 'email_already_in_use.html')