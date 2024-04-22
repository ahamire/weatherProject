from django.contrib import admin
from .models import WeatherCity, WeatherTemp  # Corrected import statements

# Register your models here.

admin.site.register(WeatherCity)
admin.site.register(WeatherTemp)
