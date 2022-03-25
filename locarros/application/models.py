import uuid
from django.db import models
from django.contrib.auth.models import User

def upload_image(request, image):
    image_extension = image.split('.')[-1]
    return f'{uuid.uuid4()}.{image_extension}'

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=11, blank=True, default='')
    birth_date = models.DateField(blank=True, default='')
    cnh = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return str(self.user)

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=7, blank=True, default='')
    year = models.IntegerField(blank=True)
    model = models.CharField(max_length=50, blank=True, default='')

    CHOICES = (
        ('sedan', 'Sedan'),
        ('coupe', 'Cupê'),
        ('sports', 'Esportivo'),
        ('crossover', 'Crossover'),
        ('hatchback', 'Hatch'),
        ('convertible', 'Conversível'),
        ('suv', 'SUV'),
        ('minivan', 'Minivan'),
        ('pickup', 'Picape'),
        ('jeep', 'Jipe')
    )

    type = models.CharField(max_length=11, blank=True, choices=CHOICES, default='')
    daily_rate = models.FloatField(blank=True)
    image = models.ImageField(upload_to=upload_image, default='default.png')
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return str(self.model)

class Location(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    lease_date = models.DateField(blank=True)
    return_date = models.DateField(blank=True)

    CHOICES = (
        ('opened', 'Em aberto'),
        ('closed', 'Fechado')
    )

    status = models.CharField(max_length=9, choices=CHOICES, default='opened')
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return str(self.status)
