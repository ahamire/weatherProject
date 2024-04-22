import urllib.request
import json
from django.shortcuts import render, redirect
from django.core.cache import cache
from .models import WeatherCity, WeatherTemp

API_KEY = '357e0f85b1de57182c417e918c88a403'  # Your API key

def fetch_weather_data(city_name, forecast=False):
    cache_key = f"weather_data_{city_name}_{forecast}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    base_url = 'http://api.openweathermap.org/data/2.5/'
    endpoint = 'weather' if not forecast else 'forecast'
    url = f'{base_url}{endpoint}?q={city_name}&units=metric&appid={API_KEY}'
    
    try:
        source = urllib.request.urlopen(url).read()
        weather_data = json.loads(source)
        cache.set(cache_key, weather_data, 3600)  # Cache data for 1 hour
        return weather_data
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP Error: {e}")
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"JSON Decode Error: {e}")
    except Exception as e:
        raise Exception(f"Error fetching weather data: {e}")

def index(request):
    data_forecast = []
    
    if request.method == 'POST':
        city_name = request.POST.get('city')
        
        if city_name:
            try:
                weather_data = fetch_weather_data(city_name)
                forecast_data = fetch_weather_data(city_name, forecast=True)
                
                if 'name' in weather_data:
                    data_forecast = [{
                        "temp": str(int(forecast_data['list'][i]['main']['temp'])) + ' °C',
                        "pressure": str(forecast_data['list'][i]['main']['pressure']),
                        "humidity": str(forecast_data['list'][i]['main']['humidity']),
                        'icon': forecast_data['list'][i]['weather'][0]['icon'],
                        'date': str(forecast_data['list'][i]['dt_txt']),
                    } for i in range(1, 40)]
                    
                    data = {
                        "country": str(weather_data['name']),
                        "coordinate": str(weather_data['coord']['lon']) + ', ' + str(weather_data['coord']['lat']),
                        "temp": str(int(weather_data['main']['temp'])) + ' °C',
                        "pressure": str(weather_data['main']['pressure']),
                        "humidity": str(weather_data['main']['humidity']),
                        'main': str(weather_data['weather'][0]['main']),
                        'description': str(weather_data['weather'][0]['description']),
                        'icon': weather_data['weather'][0]['icon'],
                    }
                    
                    # Save search history
                    WeatherCity.objects.create(city=city_name)
                    WeatherTemp.objects.create(city=city_name, temp=data['temp'], pressure=data['pressure'], humidity=data['humidity'])
                else:
                    data = {"error": "City not found"}
                    
            except KeyError as e:
                data = {"error": f"Data key not found: {e}"}
            except Exception as e:
                data = {"error": str(e)}
        else:
            data = {"error": "City name not provided"}
    else:
        data = {"error": ""}
    
    return render(request, "main/main.html", {"data": data, "data_forecast": data_forecast})
def history(request):
    cities = WeatherCity.objects.all().order_by('-timestamp')[:10]  # Get last 10 searched cities
    temps = WeatherTemp.objects.all().order_by('-timestamp')[:10]  # Get last 10 temperature records
    return render(request, "main/history.html", {"cities": cities, "temps": temps})
