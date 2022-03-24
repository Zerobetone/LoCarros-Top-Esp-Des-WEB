# Generated by Django 3.2.8 on 2022-03-19 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='default.png', upload_to=users.models.upload_user_image)),
                ('telefone_cliente', models.CharField(max_length=20)),
                ('cnh_cliente', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('cpf', models.CharField(max_length=15)),
                ('cargo', models.CharField(max_length=30)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='default.png', upload_to=users.models.upload_user_image)),
                ('telefone_cliente', models.CharField(max_length=20)),
                ('cnh_cliente', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('cpf', models.CharField(max_length=15)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]