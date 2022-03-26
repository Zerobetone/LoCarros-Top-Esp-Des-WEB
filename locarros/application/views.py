import re
import json
from datetime import datetime
from textwrap import indent
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from .models import Client, Vehicle, Location

def home(request):
    return render(request, 'home/index.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('/home')

    user = User.objects.get(id=request.user.id)

    context = {
        'user': user,
    }

    if user.is_superuser:
        return render(request, 'employee/index.html', context)

    return render(request, 'index.html', context)

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not re.search(r'^[\w]{3,20}$', username):
            return redirect('/login')

        if not re.search(r'^[\w]{3,20}$', password):
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
        
    return render(request, 'login/index.html')

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        username = request.POST['username']
        email = request.POST['email']
        telephone = request.POST['telephone']
        birth_date = request.POST['birth-date']
        cnh = request.POST['cnh']
        password = request.POST['password']

        if not re.search(r'^[a-zA-Z ]{3,50}$', first_name):
            return redirect('/register')

        if not re.search(r'^[a-zA-Z ]{3,50}$', last_name):
            return redirect('/register')

        if not re.search(r'^[\w]{3,20}$', username):
            return redirect('/register')

        if not re.search(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}$', email):
            return redirect('/register')

        if not re.search(r'^[\d]{11}$', telephone):
            return redirect('/register')

        if not re.search(r'^[\d]{4}-[\d]{2}-[\d]{2}$', birth_date):
            return redirect('/register')

        if not re.search(r'^[\d]{10}$', cnh):
            return redirect('/register')

        if not re.search(r'^[\w]{3,20}$', password):
            return redirect('/register')

        if User.objects.filter(email=email).count() > 0:
            messages.error(request, 'Este e-mail já foi cadastrado.')
            return redirect('/register')

        if User.objects.filter(username=username).count() > 0:
            messages.error(request, 'Este usuário já foi utilizado.')
            return redirect('/register')

        client = Client()
        client.user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        client.telephone = telephone
        client.birth_date = birth_date
        client.cnh = cnh
        client.user.save()
        client.save()

        messages.success(request, 'Cadastro realizado com sucesso!')

        return redirect('/login')
        
    return render(request, 'register/index.html')

@login_required(login_url='/employee/login')
def register_vehicles(request):
    if not request.user.is_superuser:
        return redirect('/')
    
    if request.method == 'POST':
        model = request.POST['model']
        license_plate = request.POST['license-plate']
        type = request.POST['type']
        year = request.POST['year']
        daily_rate = request.POST['daily-rate']
        image = request.FILES['image']
        image_extension = str(request.FILES['image']).split('.')[-1]
        description = request.POST['description']

        if not re.search(r'^[\w ]{3,50}$', model):
            return redirect('/register/vehicles')

        if not re.search(r'^[\w]{7}$', license_plate):
            return redirect('/register/vehicles')

        if not re.search(r'^(sedan|coupe|sports|crossover|hatchback|convertible|suv|minivan|pickup|jeep)$', type):
            return redirect('/register/vehicles')

        if not re.search(r'^(png|jpg|jpeg|PNG|JPG|JPEG)$', image_extension):
            return redirect('/register/vehicles')

        if not re.search(r'^[\w ]{3,255}$', description):
            return redirect('/register/vehicles')

        try:
            year = int(year)
        except:
            return redirect('/register/vehicles')

        if year < 1951 or year > datetime.now().year:
            return redirect('/register/vehicles')

        try:
            daily_rate = float(daily_rate)
        except:
            return redirect('/register/vehicles')

        vehicle = Vehicle()
        vehicle.model = model
        vehicle.license_plate = license_plate
        vehicle.type = type
        vehicle.year = year
        vehicle.daily_rate = daily_rate
        vehicle.image = image
        vehicle.description = description
        vehicle.save()

        messages.success(request, 'Cadastro realizado com sucesso!')

        return redirect('/register/vehicles')

    return render(request, 'employee/vehicles/register/index.html')

@login_required(login_url='/login')
def about(request):
    if request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'about/index.html')

@login_required(login_url='/login')
def services(request):
    if request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'services/index.html')

@login_required(login_url='/login')
def vehicles(request):
    if request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'vehicles/index.html')

@login_required(login_url='/login')
def contact(request):
    if request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'contact/index.html')

@login_required(login_url='/employee/login')
def employee_vehicles(request):
    if not request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'employee/vehicles/index.html')

def employee_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not re.search(r'^[\w]{3,20}$', username):
            return redirect('/login')

        if not re.search(r'^[\w]{3,20}$', password):
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('/')

        messages.error(request, 'Usuário ou senha inválidos.')
        
    return render(request, 'employee/login/index.html')

@login_required(login_url='/employee/login')
def employee_leases(request):
    if not request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'employee/leases/index.html')

@login_required(login_url='/employee/login')
def register_leases(request):
    if not request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'employee/leases/register/index.html')

def api(request):
    if request.method == 'GET':
        vehicles = Vehicle.objects.all()
        objects = serializers.serialize('json', vehicles)
        data = json.dumps(json.loads(objects), indent=4)
        return HttpResponse(data, content_type='application/json')
