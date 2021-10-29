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
		if u[0]['password'].strip() == password:
			# AUTHENTICATED
			if u[0]['is_superuser']:
				return render(request, 'super_user/super_user.html')
			else:
				return render(request, 'normal_user/normal_user.html')
		else:
			return render(request, 'wrong_password.html')

