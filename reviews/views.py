from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import UserForm

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('reviews:UserLogin'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to loggin and failed!")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("INVALID LOGIN DETAILS SUPPLIED")
    else:
        return render(request, 'reviews/index.html', {})    

def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()

	return render(request, 'reviews/registration.html', {'registered': registered, 'user_form': user_form})
