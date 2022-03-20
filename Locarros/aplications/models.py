from django.db import models
from  users.models import Colaborador, Cliente

class Veiculo(models.Model):
    BIS = 'BIS'
    MOTOHONDA = 'MOTOHONDA'
    BROSS = 'BROSS'
    MOTOCICLETA = 'MOTOCICLETA'
    CUPE = 'CUPE'
    CROSSOVER = 'CROSSOVER'
    ESPORTIVO = 'ESPORTIVO'
    HATCH = 'HATCH'
    JIPE = 'JIPE'
    PICAPE = 'PICAPE'
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    VAN = 'VAN E MINIVAM'

    TIPO = (
        (BIS , 'BIS'),
        (MOTOHONDA , 'MOTOHONDA'),
        ( BROSS , 'BROSS'),
        (MOTOCICLETA , 'MOTOCICLETA'),
        (CUPE, 'Cupe'),
        (CROSSOVER, 'Crossover'),
        (ESPORTIVO, 'Esportivo'),
        (HATCH, 'Hacth'),
        (JIPE, 'Jipe'),
        (PICAPE, 'Picape'),
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (VAN, 'Van/Minivam'),
    )

    DISPONIVEL = 'DISPONÍVEL'
    INDISPONIVEL = 'INDISPONÍVEL'
    STATUS_VEICULO = (
        (DISPONIVEL, 'Disponível'),
        (INDISPONIVEL,'Indisponível'),
    )

    modelo = models.CharField(max_length=200)
    cor = models.CharField(max_length=15)
    ano = models.IntegerField()
    placa = models.CharField(max_length=15)
    diaria = models.FloatField()
    tipo = models.CharField(max_length=15, choices=TIPO)
    status = models.CharField(max_length=20, choices=STATUS_VEICULO)

    def __str__(self):
        return self.modelo
class Locacao(models.Model):
    EM_ABERTO = 'EM_ABERTO'
    FECHADA = 'FECHADA'
    DEVOLUCAO_STATUS = (
        (EM_ABERTO, 'Em Aberto'),
        (FECHADA, 'Fechada'),
    )

    data_locacao = models.DateField()
    data_devolucao = models.DateField()
    status = models.CharField(max_length=10, choices = DEVOLUCAO_STATUS)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Locações'

    def __str__(self):
        return self.status