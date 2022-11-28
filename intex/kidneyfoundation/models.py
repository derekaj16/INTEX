from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Comorbidity(models.Model) :
    CONDITION = (
        ('D', 'Diabetes'),
        ('HD', 'Heart Disease'),
        ('O', 'Obesity'),
        ('HB', 'High Blood Pressure')
    )
    name = models.CharField(max_length=50, choices=CONDITION)

class Food(models.Model) :
    fcdId = models.IntegerField(primary_key=True)

class User(models.Model) :
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    email = models.EmailField(max_length=300, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    height = models.PositiveSmallIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER)
    condition = models.ManyToManyField(Comorbidity)

    entry = models.ManyToManyField(Food, through='Entry')

class Entry(models.Model) :
    MEAL_TYPE = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        ('S', 'Snack')
    )
    email = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fcdId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPE)
    quantity = models.PositiveIntegerField()
