from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from  users.models import Cliente

# Create your views here.
def index(request):
    return render(request, 'index.html')



def home(request):
    usuario_logado = request.user
    context = {'user':usuario_logado}

    return render(request,'home.html',context)