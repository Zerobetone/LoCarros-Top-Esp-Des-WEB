# Generated by Django 4.0.3 on 2022-03-24 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]