from django.contrib import admin
from .models import Client, Vehicle, Location

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['model']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['client']
