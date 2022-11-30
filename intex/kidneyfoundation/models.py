from django.db import models
from datetime import datetime

# Create your models here.
class Comorbidity(models.Model) :
    CONDITION = (
        ('D', 'Diabetes'),
        ('HD', 'Heart Disease'),
        ('O', 'Obesity'),
        ('HB', 'High Blood Pressure')
    )
    name = models.CharField(max_length=50, choices=CONDITION)

    class Meta :
        db_table = 'comorbidity'

    def __str__(self) :
        return self.name

class Food(models.Model) :
    fdcId = models.IntegerField(primary_key=True)
    


    class Meta :
        db_table = 'food'

    def __str__(self) :
        return self.fdcId

class User(models.Model) :
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    STAGE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )

    email = models.EmailField(max_length=300, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    height = models.PositiveSmallIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER)
    on_dialysis = models.BooleanField(default=True)
    stage = models.IntegerField(choices=STAGE)
    date_signed_up = models.DateField(default=datetime.today)
    user_condition = models.ManyToManyField(Comorbidity, through='Condition')
    user_entry = models.ManyToManyField(Food, through='Entry')
    k_level=models.DecimalField(max_digits=4, decimal_places=2)
    phos_level=models.DecimalField(max_digits=4, decimal_places=2)
    na_level=models.PositiveSmallIntegerField()
    creatinine_level=models.DecimalField(max_digits=4, decimal_places=2)
    albumin_level=models.DecimalField(max_digits=4, decimal_places=2)
    blood_sugar_level=models.PositiveSmallIntegerField()


    class Meta :
        db_table = 'user'

    def __str__(self) :
        return self.first_name + ' ' + self.last_name

class Condition(models.Model) :
    email = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='email')
    comId = models.ForeignKey(Comorbidity, on_delete=models.SET_NULL, null=True, db_column='comId')

    class Meta :
        db_table = 'condition'

    def __str__(self) :
        return self.comId

class Entry(models.Model) :
    MEAL_TYPE = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        ('S', 'Snack')
    )
    email = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='email')
    fdcId = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, db_column='fdcId')
    date = models.DateField()
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPE)
    quantity = models.PositiveIntegerField()

    class Meta :
        db_table = 'entry'
        unique_together = (('email', 'fdcId'))

    def __str__(self) :
        return self.date


