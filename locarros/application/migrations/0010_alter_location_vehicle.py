# Generated by Django 4.0.3 on 2022-03-27 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_remove_location_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='vehicle',
            field=models.IntegerField(),
        ),
    ]
