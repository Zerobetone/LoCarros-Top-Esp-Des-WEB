from django.contrib import admin

# Register your models here.
from .models import Veiculo, Locacao

# Register your models here.
admin.site.register(Veiculo)
admin.site.register(Locacao)