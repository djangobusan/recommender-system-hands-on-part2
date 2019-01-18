from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserForm
from .models import movie, genre, rating

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

@login_required
def details(request, movie_id):

	if request.method == 'POST':
		userId = request.user.id
		movieId = movie_id
		if rating.objects.filter(userId = userId, movieId = movieId):
			rating.objects.filter(userId = userId, movieId = movieId).delete()
		rate = request.POST.get('r')
		time = datetime.datetime.now()
		r = rating(userId=userId, movieId=movieId, rate=rate, timestamp=time)
		r.save()

	api_key = "a8a96c562bbd8c7f6f192b5cefcf9c79"
	genres = genre.objects.all().values('name').distinct()
	film = movie.objects.filter(movieId=movie_id).first()

	context_dict = {'film': film,
                    'genres': genres,
                    'api_key': api_key,
                    }

	return render(request, 'reviews/movie.html', context_dict)


@login_required
def genrePage(request, genre_id):
	if genre_id:
		selected = genre.objects.filter(name=genre_id).first()
		film = selected.movies.order_by('-year', 'movieId')
	else:
		film = movie.objects.order_by('-year', 'movieId')

	genres = genre.objects.all().values('name').distinct()

	paginator = Paginator(film, 20)
	page = request.GET.get('page')
	m = paginator.get_page(page)

	api_key = "a8a96c562bbd8c7f6f192b5cefcf9c79"

	context_dict = {'movies': m,
                    'genres': genres,
                    'api_key': api_key,
                    }

	return render(request, 'reviews/posters.html', context_dict)


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('reviews:UserLogin'))