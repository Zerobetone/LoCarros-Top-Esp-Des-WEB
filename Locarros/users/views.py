from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Cliente,Colaborador



@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    return redirect("/")


def login_user(request):
    return render(request, "registration/login.html")


def register_user(request):
    return render(request, "registration/register.html")


def login_submit(request):
    if request.method == "POST":
        user = authenticate(
            email=request.POST["email"], password=request.POST["password"]
        )

        if user is not None:
            login(request, user)
            return redirect("/login")
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return redirect("/home")


def register_submit(request):
    if request.method == "POST":
        email = User.objects.filter(email=request.POST["email"]).count()
        username = User.objects.filter(username=request.POST["username"]).count()

        if email > 0:
            messages.error(request, "Este e-mail já foi cadastrado.")

        elif username > 0:
            messages.error(request, "Este usuário já foi utilizado.")

        if email == 0 and username == 0:
            cliente = Cliente()
            cliente.user = User.objects.create_user(
                first_name=request.POST["firstname"],
                last_name=request.POST["lastname"],
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
            )
            cliente.telefone_cliente = request.POST["fone"]
            cliente.cnh_cliente= request.POST["cnh"]
            cliente.idade = request.POST["cnh"]
            cliente.cpf = request.POST["cpf"]
            cliente.user.save()
            cliente.save()
            return redirect("/login")

    return redirect("/register")

def register_colaborador_submit(request):
    if request.method == "POST":
        email = User.objects.filter(email=request.POST["email"]).count()
        username = User.objects.filter(username=request.POST["username"]).count()

        if email > 0:
            messages.error(request, "Este e-mail já foi cadastrado.")

        elif username > 0:
            messages.error(request, "Este usuário já foi utilizado.")

        if email == 0 and username == 0:
            cliente = Cliente()
            cliente.user = User.objects.create_user(
                first_name=request.POST["firstname"],
                last_name=request.POST["lastname"],
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
            )
            cliente.telefone_cliente = request.POST["fone"]
            cliente.cnh_cliente= request.POST["cnh"]
            cliente.idade = request.POST["cnh"]
            cliente.cpf = request.POST["cpf"]
            cliente.user.save()
            cliente.save()
            return redirect("/login_colaborador")

    return redirect("/register_colaborador")




