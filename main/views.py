import urllib.request
import json
from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')

        if city:
            try:
                source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                                city + '&units=metric&appid=6f53276f4587b6894160bf89f754b84e').read()
                weather_data = json.loads(source)
                source_hour = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/forecast?q=' +
                                                city + '&units=metric&appid=d998f65fff1b4b90e3c7d80a085c67e7').read()
                weather_data_hour = json.loads(source_hour)
                if 'name' in weather_data:
                    data = {
                        "country": str(weather_data['name']),
                        "coordinate": str(weather_data['coord']['lon']) + ', ' + str(weather_data['coord']['lat']),
                        "temp": str(weather_data['main']['temp']) + ' °C',
                        "pressure": str(weather_data['main']['pressure']),
                        "humidity": str(weather_data['main']['humidity']),
                        'main': str(weather_data['weather'][0]['main']),
                        'description': str(weather_data['weather'][0]['description']),
                        'icon': weather_data['weather'][0]['icon'],
                    }
                    print(data)
                    hour_data = {
                        
                    }
                else:
                    data = {"error": "City not found"}
            except Exception as e:
                data = {"error": "Error fetching weather data: " + str(e)}
        else:
            data = {"error": "City name not provided"}
    else:
        data = {"error": "Error fetching weather data"}

    return render(request, "main/index.html", data)
