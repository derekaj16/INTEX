# Generated by Django 4.1.3 on 2022-12-01 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kidneyfoundation', '0002_alter_entry_time_alter_user_height'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blood_pressure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='diabetes',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='entry',
            name='time',
            field=models.TimeField(default=datetime.time(14, 34, 51, 539600)),
        ),
    ]