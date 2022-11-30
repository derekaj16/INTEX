# Generated by Django 4.1.3 on 2022-11-30 17:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comorbidity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('D', 'Diabetes'), ('HD', 'Heart Disease'), ('O', 'Obesity'), ('HB', 'High Blood Pressure')], max_length=50)),
            ],
            options={
                'db_table': 'comorbidity',
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comId', models.ForeignKey(db_column='comId', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kidneyfoundation.comorbidity')),
            ],
            options={
                'db_table': 'condition',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meal_type', models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner'), ('S', 'Snack')], max_length=1)),
                ('quantity', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'entry',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('fdcId', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('k', models.DecimalField(decimal_places=3, max_digits=8)),
                ('na', models.DecimalField(decimal_places=3, max_digits=8)),
                ('phos', models.DecimalField(decimal_places=3, max_digits=8)),
                ('protein', models.DecimalField(decimal_places=3, max_digits=8)),
            ],
            options={
                'db_table': 'food',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=300, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('birthday', models.DateField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('on_dialysis', models.BooleanField(default=True)),
                ('stage', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('date_signed_up', models.DateField(default=datetime.datetime.today)),
                ('k_level', models.DecimalField(decimal_places=2, default=4.4, max_digits=4)),
                ('phos_level', models.DecimalField(decimal_places=2, default=3.65, max_digits=4)),
                ('na_level', models.PositiveSmallIntegerField(default=140)),
                ('creatinine_level', models.DecimalField(decimal_places=2, default=1.2, max_digits=4)),
                ('albumin_level', models.DecimalField(decimal_places=2, default=3.5, max_digits=4)),
                ('blood_sugar_level', models.PositiveSmallIntegerField(default=85)),
                ('user_condition', models.ManyToManyField(through='kidneyfoundation.Condition', to='kidneyfoundation.comorbidity')),
                ('user_entry', models.ManyToManyField(through='kidneyfoundation.Entry', to='kidneyfoundation.food')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='email',
            field=models.ForeignKey(db_column='email', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kidneyfoundation.user'),
        ),
        migrations.AddField(
            model_name='entry',
            name='fdcId',
            field=models.ForeignKey(db_column='fdcId', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kidneyfoundation.food'),
        ),
        migrations.AddField(
            model_name='condition',
            name='email',
            field=models.ForeignKey(db_column='email', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kidneyfoundation.user'),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together={('email', 'fdcId')},
        ),
    ]
