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
    path('employee/login/', views.employee_login, name='employee-login'),
    path('employee/leases/', views.employee_leases, name='employee-leases'),
    path('employee/clients/', views.employee_clients, name='employee-clients'),
    path('employee/edit/client/<int:id>/', views.edit_client, name='employee-edit-client'),
    path('employee/delete/client/<int:id>/', views.delete_client, name='employee-delete-client'),
    path('employee/vehicles/', views.employee_vehicles, name='employee-vehicles'),
    path('register/vehicles/', views.register_vehicles, name='register-vehicles'),
    path('register/leases/', views.register_leases, name='register-leases'),
    path('api/', views.api, name='api'),
]
