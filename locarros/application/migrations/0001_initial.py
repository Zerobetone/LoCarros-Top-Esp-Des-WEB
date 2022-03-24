# Generated by Django 4.0.3 on 2022-03-23 16:41

import application.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(blank=True, default='', max_length=7)),
                ('year', models.IntegerField(blank=True)),
                ('model', models.CharField(blank=True, default='', max_length=50)),
                ('type', models.CharField(blank=True, choices=[('sedan', 'Sedan'), ('coupe', 'Cupê'), ('sports', 'Esportivo'), ('crossover', 'Crossover'), ('hatchback', 'Hatch'), ('convertible', 'Conversível'), ('suv', 'SUV'), ('minivan', 'Minivan'), ('pickup', 'Picape'), ('jeep', 'Jipe')], default='', max_length=11)),
                ('daily_rate', models.FloatField(blank=True)),
                ('image', models.ImageField(default='default.png', upload_to=application.models.upload_image)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(blank=True, default='', max_length=11)),
                ('birth_date', models.DateField(blank=True, default='')),
                ('cnh', models.CharField(blank=True, default='', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]