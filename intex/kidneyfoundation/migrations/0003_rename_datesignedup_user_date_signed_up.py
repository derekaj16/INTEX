# Generated by Django 4.1.3 on 2022-11-28 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kidneyfoundation', '0002_user_datesignedup_user_on_dialysis_user_stage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='dateSignedUp',
            new_name='date_signed_up',
        ),
    ]