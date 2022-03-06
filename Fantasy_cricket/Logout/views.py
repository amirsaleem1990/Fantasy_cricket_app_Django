from django.http import HttpResponse

def logout(request):
	# request.session['logged_in'] = False
	request.session.flush()
	return HttpResponse("Logged out")
