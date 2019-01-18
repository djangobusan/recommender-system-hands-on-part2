from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
	path('', views.index, name='UserLogin'),
	path('register/', views.register, name='Registration'),
	path('info/<int:movie_id>/', views.details, name='MovieDetails'),
	path('genre/<str:genre_id>/', views.genrePage, name='MovieGenre'),
]