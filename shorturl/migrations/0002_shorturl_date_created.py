# Generated by Django 4.0.9 on 2023-02-17 05:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorturl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]