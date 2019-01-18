from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
	path('', views.index, name='UserLogin'),
	path('register/', views.register, name='Registration'),	
]