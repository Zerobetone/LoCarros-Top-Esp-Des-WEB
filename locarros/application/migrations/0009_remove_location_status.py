# Generated by Django 4.0.3 on 2022-03-27 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_location_daily_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='status',
        ),
    ]