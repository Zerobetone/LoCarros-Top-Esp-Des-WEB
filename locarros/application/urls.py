"""locarros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('contact/', views.contact, name='contact'),
    path('details/vehicle/<int:id>/', views.vehicle_details, name='vehicle-details'),

    path('employee/login/', views.employee_login, name='employee-login'),
    path('employee/leases/', views.employee_leases, name='employee-leases'),
    path('employee/clients/', views.employee_clients, name='employee-clients'),
    path('employee/vehicles/', views.employee_vehicles, name='employee-vehicles'),
    path('employee/edit/lease/<int:id>/', views.edit_lease, name='employee-edit-lease'),
    path('employee/edit/client/<int:id>/', views.edit_client, name='employee-edit-client'),
    path('employee/edit/vehicle/<int:id>/', views.edit_vehicle, name='employee-edit-vehicle'),
    path('employee/delete/lease/<int:id>/', views.delete_lease, name='employee-delete-lease'),
    path('employee/delete/client/<int:id>/', views.delete_client, name='employee-delete-client'),
    path('employee/delete/vehicle/<int:id>/', views.delete_vehicle, name='employee-delete-vehicle'),

    path('register/vehicles/', views.register_vehicles, name='register-vehicles'),
    path('register/leases/', views.register_leases, name='register-leases'),

    path('api/vehicles/', views.api_vehicles, name='api-vehicles'),
    path('api/vehicle/<int:id>/', views.api_vehicle, name='api-vehicle'),
]
