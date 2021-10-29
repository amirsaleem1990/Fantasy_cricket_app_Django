from django.shortcuts import render
from Login.models import User

def create_user(request):

	email_address = request.POST.get('email_address', None) 
	full_name = request.POST.get('full_name', None)
	password = request.POST.get('password', None)
	retype_password = request.POST.get('retype_password', None)
	# if password != retype_password:
		# ERROR???

	u = User.objects.filter(email=email_address).values()
	if not u:
		# Create an user
		u = User(email=email_address, 
				 full_name=full_name, 
				 password=password
				 )
		u.save()
		return render(request, 'user_created.html')
	else:
		return render(request, 'email_already_in_use.html')