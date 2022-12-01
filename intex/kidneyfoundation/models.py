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
    food_name = models.CharField(max_length=100)
    serving_size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    serving_size_unit = models.CharField(max_length=10, null=True, blank=True)
    k_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    na_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    phos_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    protien_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fat_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    carbs_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    calories = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta :
        db_table = 'food'

    def __str__(self) :
        sString = self.food_name + " " + str(self.fdcID)
        return sString

class Entry(models.Model) :
    MEAL_TYPE = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        ('S', 'Snack')
    )
    entry_id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.today)
    time = models.TimeField(default=datetime.today().time())
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPE)
    num_servings = models.DecimalField(max_digits=7, decimal_places=2)
    email = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, db_column='email')
    fdcId = models.ForeignKey('Food', on_delete=models.SET_NULL, null=True, db_column='fdcId')

    class Meta :
        db_table = 'entry'

    def __str__(self) :
        sString = self.email + " " + self.date + " " + self.meal_type
        return sString

    class Meta :
        db_table = 'entry'
        unique_together = (('email', 'fdcId', 'date', 'time'))

    def __str__(self) :
        return self.date


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
    password = models.CharField(max_length=50, default='password')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    height = models.IntegerField()
    weight = models.FloatField()
    gender = models.CharField(max_length=1, choices=GENDER)
    on_dialysis = models.BooleanField(default=True)
    diabetes = models.BooleanField(default=False)
    blood_pressure = models.BooleanField(default=False)
    stage = models.IntegerField(choices=STAGE)
    date_signed_up = models.DateField(default=datetime.today)
    user_condition = models.ManyToManyField(Comorbidity, through='Condition')
    user_entry = models.ManyToManyField(Food, through='Entry')

    k_level=models.DecimalField(max_digits=4, decimal_places=2, default=4.4)
    phos_level=models.DecimalField(max_digits=4, decimal_places=2, default=3.65)
    na_level=models.PositiveSmallIntegerField(default=140)
    creatinine_level=models.DecimalField(max_digits=4, decimal_places=2, default=1.2)
    albumin_level=models.DecimalField(max_digits=4, decimal_places=2, default=3.5)
    blood_sugar_level=models.PositiveSmallIntegerField(default=85)


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




