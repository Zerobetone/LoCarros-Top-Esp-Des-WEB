from django.db import models
from django.contrib.auth.models import User



def upload_user_image(request, file_name):
    return f"{request.user}-{file_name}"


class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(upload_to=upload_user_image, default="default.png")
    telefone_cliente = models.CharField(max_length=20)
    cnh_cliente = models.CharField(max_length=100)
    idade = models.IntegerField()
    cpf = models.CharField(max_length=15)



    def __str__(self):
        return str(self.user)

class Colaborador(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(upload_to=upload_user_image, default="default.png")
    telefone_cliente = models.CharField(max_length=20)
    cnh_cliente = models.CharField(max_length=100)
    idade = models.IntegerField()
    cpf = models.CharField(max_length=15)
    cargo = models.CharField(max_length=30)



    def __str__(self):
        return str(self.user)

