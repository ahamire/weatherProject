from django.db import models

class WeatherCity(models.Model):  # Corrected model name
    city = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city

class WeatherTemp(models.Model):  # Corrected model name
    city = models.CharField(max_length=255)
    temp = models.CharField(max_length=50)
    pressure = models.CharField(max_length=50)
    humidity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temp} - {self.timestamp}"
