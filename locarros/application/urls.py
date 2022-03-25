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
from .views import * 

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('vehicles/', vehicles, name='vehicles'),
    path('contact/', contact, name='contact'),
    path('employee/login/', employee_login, name='employee-login'),
    path('employee/vehicles/', employee_vehicles, name='employee-vehicles'),
    path('register/vehicles/', register_vehicles, name='register-vehicles'),
]
