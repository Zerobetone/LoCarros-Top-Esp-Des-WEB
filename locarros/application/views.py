import os
import re
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from .models import Client, Vehicle, Location

def home(request):
    vehicles = Vehicle.objects.all()

    context = {
        'vehicles': vehicles
    }

    return render(request, 'home/index.html', context)

def index(request):
    if not request.user.is_authenticated:
        return redirect('/home')

    user = User.objects.get(id=request.user.id)
    vehicles = Vehicle.objects.all()

    context = {
        'user': user,
        'vehicles': vehicles
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

        try:
            client = Client()
            client.user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            client.telephone = telephone
            client.birth_date = birth_date
            client.cnh = cnh
            client.user.save()
            client.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
        except Exception:
            messages.error(request, 'Ocorreu algum erro ao cadastrar.')

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

        try:
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
        except Exception:
            messages.error(request, 'Ocorreu algum erro ao cadastrar.')

        return redirect('/register/vehicles')

    return render(request, 'employee/vehicles/register/index.html')

@login_required(login_url='/employee/login')
def edit_vehicle(request, id):
    if not request.user.is_superuser:
        return redirect('/')

    if not re.search(r'^[\d]+$', str(id)):
        return redirect('/')

    if not Vehicle.objects.filter(id=id).count():
        return redirect('/')
    
    if request.method == 'POST':
        model = request.POST['model']
        license_plate = request.POST['license-plate']
        type = request.POST['type']
        year = request.POST['year']
        daily_rate = request.POST['daily-rate']
        description = request.POST['description']

        try:
            image = request.FILES['image']
        except Exception:
            image = ""
        
        image_extension = str(image).split('.')[-1]

        if not re.search(r'^[\w ]{3,50}$', model):
            return redirect(f'/employee/edit/vehicle/{id}')

        if not re.search(r'^[\w]{7}$', license_plate):
            return redirect(f'/employee/edit/vehicle/{id}')

        if not re.search(r'^(sedan|coupe|sports|crossover|hatchback|convertible|suv|minivan|pickup|jeep)$', type):
            return redirect(f'/employee/edit/vehicle/{id}')

        if image_extension:
            if not re.search(r'^(png|jpg|jpeg|PNG|JPG|JPEG)$', image_extension):
                return redirect(f'/employee/edit/vehicle/{id}')

        if not re.search(r'^[\w ]{3,255}$', description):
            return redirect(f'/employee/edit/vehicle/{id}')

        try:
            year = int(year)
        except:
            return redirect(f'/employee/edit/vehicle/{id}')

        if year < 1951 or year > datetime.now().year:
            return redirect(f'/employee/edit/vehicle/{id}')

        try:
            daily_rate = daily_rate.replace(',', '.', 1)
            daily_rate = float(daily_rate)
        except:
            return redirect(f'/employee/edit/vehicle/{id}')

        try:
            if image_extension:
                vehicle = Vehicle.objects.get(id=id)

                if os.path.exists(vehicle.image.path):
                    os.remove(vehicle.image.path)

                vehicle.model = model
                vehicle.license_plate = license_plate
                vehicle.type = type
                vehicle.year = year
                vehicle.daily_rate = daily_rate
                vehicle.image = image
                vehicle.description = description
                vehicle.save()
            else:
                Vehicle.objects.filter(id=id).update(model=model, license_plate=license_plate, type=type, year=year, daily_rate=daily_rate, description=description)

            messages.success(request, 'Dados atualizados com sucesso!')
        except Exception:
            messages.error(request, 'Ocorreu algum erro ao atualizar os dados.')

        return redirect(f'/employee/edit/vehicle/{id}')

    vehicle = Vehicle.objects.filter(id=id)[0]

    context = {
        'vehicle': vehicle
    }

    return render(request, 'employee/vehicles/edit/index.html', context)

@login_required(login_url='/employee/login')
def delete_vehicle(request, id):
    if not request.user.is_superuser:
        return redirect('/')
    
    if not re.search(r'^[\d]+$', str(id)):
        return redirect('/employee/vehicles')

    if not Vehicle.objects.filter(id=id).count():
        messages.error(request, 'Este veículo não existe.')
        return redirect('/employee/vehicles')

    try:
        Vehicle.objects.filter(id=id).delete()
        messages.success(request, 'Veículo excluído com sucesso!')
    except Exception:
        messages.error(request, 'Ocorreu algum erro ao excluir o veículo.')

    return redirect('/employee/vehicles')

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

    vehicles = Vehicle.objects.all()

    context = {
        'vehicles': vehicles
    }
    
    return render(request, 'vehicles/index.html', context)

@login_required(login_url='/login')
def vehicle_details(request, id):
    if not re.search(r'^[\d]+$', str(id)):
        return redirect('/')

    if not Vehicle.objects.filter(id=id).count():
        return redirect('/')

    user = User.objects.get(id=request.user.id)
    vehicle = Vehicle.objects.filter(id=id)[0]

    context = {
        'user': user,
        'vehicle': vehicle
    }

    return render(request, 'vehicles/details/index.html', context)

@login_required(login_url='/login')
def contact(request):
    if request.user.is_superuser:
        return redirect('/')
    
    return render(request, 'contact/index.html')

@login_required(login_url='/employee/login')
def employee_vehicles(request):
    if not request.user.is_superuser:
        return redirect('/')

    vehicles = []

    if request.method == 'POST':
        option = request.POST['option']
        search = request.POST['search']

        if option == "id":
            if not re.search(r'^[\d]+$', search):
                return redirect('/employee/vehicles')

            vehicles = Vehicle.objects.filter(id=search)

        elif option == "model":
            if not re.search(r'^[\w ]{3,255}$', search):
                return redirect('/employee/vehicles')

            vehicles = Vehicle.objects.filter(model__icontains=search)

        elif option == "license-plate":
            if not re.search(r'^[\w ]{1,7}$', search):
                return redirect('/employee/vehicles')

            vehicles = Vehicle.objects.filter(license_plate__icontains=search)

        elif option == "type":
            if not re.search(r'^[A-Za-z]{3,11}$', search):
                return redirect('/employee/vehicles')

            type = ""

            if "sedan" in search.lower():
                type = "sedan"
            elif "cupê" in search.lower():
                type = "coupe"
            elif "esportivo" in search.lower():
                type = "sports"
            elif "crossover" in search.lower():
                type = "crossover"
            elif "hatchback" in search.lower():
                type = "hatchback"
            elif "conversível" in search.lower():
                type = "convertible"
            elif "suv" in search.lower():
                type = "suv"
            elif "minivan" in search.lower():
                type = "minivan"
            elif "picape" in search.lower():
                type = "pickup"
            elif "jipe" in search.lower():
                type = "jeep"
            else:
                return redirect('/employee/vehicles')

            vehicles = Vehicle.objects.filter(type__icontains=type)
        
        elif option == "year":
            if not re.search(r'^[\d]{4}$', search):
                return redirect('/employee/vehicles')

            vehicles = Vehicle.objects.filter(year=search)

        elif option == "description":
            if not re.search(r'^[\w ]{3,255}$', search):
                return redirect('/employee/vehicles')

            vehicles = Vehicle.objects.filter(description_icontains=search)

        context = {
            'vehicles': vehicles
        }

        return render(request, 'employee/vehicles/index.html', context)
    
    vehicles = Vehicle.objects.all()

    context = {
        'vehicles': vehicles
    }
    
    return render(request, 'employee/vehicles/index.html', context)

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

    locations = []

    if request.method == 'POST':
        option = request.POST['option']
        search = request.POST['search']

        if option == "id":
            if not re.search(r'^[\d]+$', search):
                return redirect('/employee/leases')

            locations = Location.objects.filter(id=search)

        elif option == "client":
            if not re.search(r'^[A-Za-z ]{3,255}$', search):
                return redirect('/employee/leases')

            users = []
            first_name = search.split(' ')[0]
            last_name = ' '.join(search.split(' ')[1:])

            if not last_name:
                users = User.objects.filter(first_name__icontains=first_name)
            else:
                users = User.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)

            for user in users:
                client = Client.objects.get(user=user.id)
                location = Location.objects.filter(client=client)

                if location:
                    locations.append(location[0])

        elif option == "vehicle":
            if not re.search(r'^[\w ]{3,255}$', search):
                return redirect('/employee/leases')

            vehicles = Vehicle.objects.filter(model__icontains=search)

            for vehicle in vehicles:
                location = Location.objects.get(vehicle=vehicle.id)
                locations.append(location)

        elif option == "lease-date":
            if not re.search(r'^[\d]{2}/[\d]{2}/[\d]{4}$', search):
                return redirect('/employee/leases')

            formatted_date = search.split('/')[2] + '-' + search.split('/')[1] + '-' + search.split('/')[0]

            locations = Location.objects.filter(lease_date=formatted_date)

        elif option == "due-date":
            if not re.search(r'^[\d]{2}/[\d]{2}/[\d]{4}$', search):
                return redirect('/employee/leases')

            formatted_date = search.split('/')[2] + '-' + search.split('/')[1] + '-' + search.split('/')[0]

            locations = Location.objects.filter(due_date=formatted_date)

        context = {
            'locations': locations
        }

        return render(request, 'employee/leases/index.html', context)
    
    locations = Location.objects.all()

    context = {
        'locations': locations
    }

    return render(request, 'employee/leases/index.html', context)

@login_required(login_url='/employee/login')
def register_leases(request):
    if not request.user.is_superuser:
        return redirect('/')
    
    if request.method == 'POST':
        client_id = request.POST['client']
        vehicle_id = request.POST['vehicle']
        lease_date = request.POST['lease-date']
        due_date = request.POST['due-date']
        daily_rate = request.POST['daily-rate']
        total = request.POST['total']
        description = request.POST['description']

        if not re.search(r'^[\d]+$', client_id):
            return redirect('/register/leases')

        if not re.search(r'^[\d]+$', vehicle_id):
            return redirect('/register/leases')

        if not re.search(r'^[\d]{4}-[\d]{2}-[\d]{2}$', lease_date):
            return redirect('/register/leases')

        if not re.search(r'^[\d]{4}-[\d]{2}-[\d]{2}$', due_date):
            return redirect('/register/leases')

        if not re.search(r'^[\w ]{3,255}$', description):
            return redirect('/register/leases')

        try:
            total = float(total)
            daily_rate = float(daily_rate)
        except:
            return redirect('/register/leases')

        client = Client.objects.get(id=client_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)

        try:
            location = Location()
            location.client = client
            location.vehicle = vehicle
            location.lease_date = lease_date
            location.due_date = due_date
            location.daily_rate = daily_rate
            location.total = total
            location.description = description
            location.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
        except Exception:
            messages.error(request, 'Ocorreu algum erro ao cadastrar.')

        return redirect('/register/leases')

    clients = Client.objects.all()
    vehicles = Vehicle.objects.all()

    context = {
        'clients': clients,
        'vehicles': vehicles
    }

    return render(request, 'employee/leases/register/index.html', context)

@login_required(login_url='/employee/login')
def employee_clients(request):
    if not request.user.is_superuser:
        return redirect('/')

    clients = []

    if request.method == 'POST':
        option = request.POST['option']
        search = request.POST['search']

        if option == "id":
            if not re.search(r'^[\d]$', search):
                return redirect('/employee/clients')

            user = User.objects.get(id=int(search))
            clients = Client.objects.filter(user=user)

        elif option == "name":
            if not re.search(r'^[\w ]{1,255}$', search):
                return redirect('/employee/clients')

            users = []
            first_name = search.split(' ')[0]
            last_name = ' '.join(search.split(' ')[1:])

            if not last_name:
                users = User.objects.filter(first_name__icontains=first_name)
            else:
                users = User.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)

            for user in users:
                client = Client.objects.get(user=user.id)
                clients.append(client)

        elif option == "username":
            if not re.search(r'^[\w]{3,20}$', search):
                return redirect('/employee/clients')

            user = User.objects.get(username=search)
            clients = Client.objects.filter(user=user)

        elif option == "email":
            if not re.search(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}$', search):
                return redirect('/employee/clients')

            user = User.objects.get(email=search)
            clients = Client.objects.filter(user=user)

        elif option == "telephone":
            if not re.search(r'^[\d]{11}$', search):
                return redirect('/employee/clients')

            clients = Client.objects.filter(telephone=search)

        elif option == "cnh":
            if not re.search(r'^[\d]{10}$', search):
                return redirect('/employee/clients')

            clients = Client.objects.filter(cnh=search) 

        elif option == "birth-date":
            if not re.search(r'^[\d]{2}/[\d]{2}/[\d]{4}$', search):
                return redirect('/employee/clients')

            formatted_date = search.split('/')[2] + '-' + search.split('/')[1] + '-' + search.split('/')[0]

            clients = Client.objects.filter(birth_date=formatted_date) 
        else:
            return redirect('/employee/clients')

        context = {
            'clients': clients
        }

        return render(request, 'employee/clients/index.html', context)

    clients = Client.objects.all()

    context = {
        'clients': clients
    }
    
    return render(request, 'employee/clients/index.html', context)

@login_required(login_url='/employee/login')
def edit_client(request, id):
    if not request.user.is_superuser:
        return redirect('/')
    
    if not re.search(r'^[\d]+$', str(id)):
        return redirect('/employee/clients')

    if not User.objects.filter(id=id).count():
        messages.error(request, 'Este usuário não existe.')
        return redirect('/employee/clients')

    user = User.objects.get(id=id)
    client = Client.objects.filter(user=user)[0]
    
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        username = request.POST['username']
        email = request.POST['email']
        telephone = request.POST['telephone']
        birth_date = request.POST['birth-date']
        cnh = request.POST['cnh']

        if not re.search(r'^[a-zA-Z ]{3,50}$', first_name):
            return redirect(f'/employee/edit/client/{id}')

        if not re.search(r'^[a-zA-Z ]{3,50}$', last_name):
            return redirect(f'/employee/edit/client/{id}')

        if not re.search(r'^[\w]{3,20}$', username):
            return redirect(f'/employee/edit/client/{id}')

        if not re.search(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}$', email):
            return redirect(f'/employee/edit/client/{id}')

        if not re.search(r'^[\d]{11}$', telephone):
            return redirect(f'/employee/edit/client/{id}')

        if not re.search(r'^[\d]{4}-[\d]{2}-[\d]{2}$', birth_date):
            return redirect(f'/employee/edit/client/{id}')

        if not re.search(r'^[\d]{10}$', cnh):
            return redirect(f'/employee/edit/client/{id}')

        if email != user.email: 
            if User.objects.filter(email=email).count() > 0:
                messages.error(request, 'Este e-mail já foi cadastrado.')
                return redirect(f'/employee/edit/client/{id}')

        if username != user.username: 
            if User.objects.filter(username=username).count() > 0:
                messages.error(request, 'Este usuário já foi utilizado.')
                return redirect(f'/employee/edit/client/{id}')

        try:
            User.objects.filter(id=id).update(first_name=first_name, last_name=last_name, username=username, email=email)
            Client.objects.filter(user=user).update(telephone=telephone, birth_date=birth_date, cnh=cnh)
            messages.success(request, 'Dados atualizados com sucesso!')
        except Exception:
            messages.error(request, 'Ocorreu algum erro ao atualizar os dados.')

        return redirect(f'/employee/edit/client/{id}')

    context = {
        'client': client
    }
    
    return render(request, 'employee/clients/edit/index.html', context)

@login_required(login_url='/employee/login')
def edit_lease(request, id):
    if not request.user.is_superuser:
        return redirect('/')
    
    if not re.search(r'^[\d]+$', str(id)):
        return redirect('/employee/leases')

    if not Location.objects.filter(id=id).count():
        messages.error(request, 'Essa locação não existe.')
        return redirect('/employee/leases')
    
    if request.method == 'POST':
        client_id = request.POST['client']
        vehicle_id = request.POST['vehicle']
        lease_date = request.POST['lease-date']
        due_date = request.POST['due-date']
        daily_rate = request.POST['daily-rate']
        total = request.POST['total']
        description = request.POST['description']

        if not re.search(r'^[\d]+$', client_id):
            return redirect('/employee/leases')

        if not re.search(r'^[\d]+$', vehicle_id):
            return redirect('/employee/leases')

        if not re.search(r'^[\d]{4}-[\d]{2}-[\d]{2}$', lease_date):
            return redirect('/employee/leases')

        if not re.search(r'^[\d]{4}-[\d]{2}-[\d]{2}$', due_date):
            return redirect('/employee/leases')

        if not re.search(r'^[\w ]{3,255}$', description):
            return redirect('/employee/leases')

        try:
            total = float(total)
            daily_rate = float(daily_rate)
        except:
            return redirect('/employee/leases')

        client = Client.objects.get(id=client_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)

        try:
            Location.objects.filter(id=id).update(client=client, vehicle=vehicle, lease_date=lease_date, due_date=due_date, daily_rate=daily_rate, total=total, description=description)
            messages.success(request, 'Dados atualizados com sucesso!')
        except Exception:
            messages.error(request, 'Ocorreu algum erro ao atualizar os dados.')

        return redirect(f'/employee/edit/lease/{id}')

    clients = Client.objects.all()
    vehicles = Vehicle.objects.all()
    location = Location.objects.get(id=id)

    context = {
        'clients': clients,
        'vehicles': vehicles,
        'location': location
    }
    
    return render(request, 'employee/leases/edit/index.html', context)

@login_required(login_url='/employee/login')
def delete_client(request, id):
    if not request.user.is_superuser:
        return redirect('/')
    
    if not re.search(r'^[\d]+$', str(id)):
        return redirect('/employee/clients')

    if not User.objects.filter(id=id).count():
        messages.error(request, 'Este usuário não existe.')
        return redirect('/employee/clients')

    try:
        User.objects.filter(id=id).delete()
        messages.success(request, 'Cliente excluído com sucesso!')
    except Exception:
        messages.error(request, 'Ocorreu algum erro ao excluir o usuário.')

    return redirect('/employee/clients')

@login_required(login_url='/employee/login')
def delete_lease(request, id):
    if not request.user.is_superuser:
        return redirect('/')
    
    if not re.search(r'^[\d]+$', str(id)):
        return redirect('/employee/leases')

    if not Location.objects.filter(id=id).count():
        messages.error(request, 'Essa locação não existe.')
        return redirect('/employee/leases')

    try:
        Location.objects.filter(id=id).delete()
        messages.success(request, 'Locação excluída com sucesso!')
    except Exception:
        messages.error(request, 'Ocorreu algum erro ao excluir a locação.')

    return redirect('/employee/leases')

def api_vehicle(request, id):
    if not re.search(r'^[\d]+$', str(id)):
        objects = []
        data = json.dumps(objects, indent=4)
        return HttpResponse(data, content_type='application/json')
    
    if request.method == 'GET':
        vehicles = Vehicle.objects.filter(id=id)
        objects = serializers.serialize('json', vehicles)
        data = json.dumps(json.loads(objects), indent=4)
        return HttpResponse(data, content_type='application/json')

def api_vehicles(request):
    if request.method == 'GET':
        vehicles = Vehicle.objects.all()
        objects = serializers.serialize('json', vehicles)
        data = json.dumps(json.loads(objects), indent=4)
        return HttpResponse(data, content_type='application/json')
