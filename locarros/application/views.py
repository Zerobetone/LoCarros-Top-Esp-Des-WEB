from pydoc import cli
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Client, Vehicle, Location

def home(request):
    return render(request, 'home/index.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('/home')

    user = User.objects.get(id=request.user.id)
    client = Client.objects.get(user=user)

    context = {
        'user': user,
        'client': client
    }

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
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        telephone = request.POST['telephone']
        birth_date = request.POST['birth-date']
        cnh = request.POST['cnh']
        password = request.POST['password']

        if not re.search(r'^[a-zA-Z ]{3,50}$', name):
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
        client.user = User.objects.create_user(first_name=name, username=username, email=email, password=password)
        client.telephone = telephone
        client.birth_date = birth_date
        client.cnh = cnh
        client.user.save()
        client.save()

        return redirect('/login')
        
    return render(request, 'register/index.html')
