import requests
from django.shortcuts import render
from .models import WeatherSearch


def get_weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        api_key = ''
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(api_url)
        weather_data = response.json()

        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']

        weather_search = WeatherSearch(
            city=city,
            temperature=temperature,
            description=description,
            icon=icon
        )
        weather_search.save()

        context = {
            'city': city,
            'temperature': temperature,
            'description': description,
            'icon': icon
        }
        return render(request, 'weather/weather.html', context)

    return render(request, 'weather/weather.html')



def get_weather_history(request):
    recent_searches = WeatherSearch.objects.order_by('-search_time')[:5]

    context = {
        'recent_searches': recent_searches
    }
    return render(request, 'weather/history.html', context)
