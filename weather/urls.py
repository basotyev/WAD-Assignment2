from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_weather, name='get-weather'),
    path('history/', views.get_weather_history, name='weather-history'),
]
