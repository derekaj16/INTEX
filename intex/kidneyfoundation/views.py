from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from kidneyfoundation.models import * # need to make model for this
from datetime import datetime, timedelta
from decimal import Decimal


# feet/inches to centimeters Function
def heightToCm(feet, inches) :
    cm = ((float(feet) * 12) + float(inches)) * 2.54
    return round(cm, 2)

# Pounds to Kilograms Function
def lbsToKg(lbs) :
    kg = float(lbs) * 0.453592
    return round(kg, 2)

# Create your views here.
def indexPageView(request, error=False) :
    context = {
        'error' : error,
        'errorMessage' : 'Sorry. We couldn\'t find a user with your email :/'
    }
    
    return render(request, 'kidneyfoundation/index.html', context)


def addUserPageView(request) :
    if request.method == 'POST' :
        user = User()
        user.email = request.POST[ 'email' ]
        user.password = request.POST['password']
        user.first_name = request.POST[ 'first_name' ]
        user.last_name = request.POST[ 'last_name' ]
        user.birthday = request.POST[ 'birthday' ]
        user.height = heightToCm(request.POST[ 'feet' ], request.POST['inches'])
        user.weight = lbsToKg(request.POST[ 'weight' ])
        user.gender = request.POST[ 'gender' ]
        user.date_signed_up = datetime.now()
        user.on_dialysis = request.POST[ 'on_dialysis' ]
        user.stage = request.POST[ 'stage' ]
        user.k_level = request.POST[ 'k_level' ]
        user.na_level = request.POST[ 'na_level' ]
        user.phos_level = request.POST[ 'phos_level' ]
        user.creatinine_level = request.POST[ 'creatinine_level' ]
        user.albumin_level = request.POST[ 'albumin_level' ]
        user.blood_sugar_level = request.POST[ 'blood_sugar_level' ]
        
        user.save()

        return indexPageView(request)
    else: 
        return render(request, 'kidneyfoundation/addUser.html')


def LoginView(request) :
    isError = False

    if request.method == 'POST' :
        email = request.POST['email']
        password = request.POST['password']

        allUsers = User.objects.all()

        for current_user in allUsers :
            if email == current_user.email and password == current_user.password :
                # get the user object with that email
                user = User.objects.get(email=email)

                # store that user's email to session storage
                request.session['email'] = user.email

                # Then get that email as a variable called email
                # email = request.session.get('email', 'davemurdock55@gmail.com')
                
                # Then go and render the homepage, passing the session variable as the value for the email key in a nameless dictionary
                return homePageView(request)
            else :
                isError = True

    return indexPageView(request, isError)

def LogoutView(request) :
    request.session['email'] = None
    return render(request, 'kidneyfoundation/index.html')

# def signInPageView(request) :

#     if request.method == 'POST' :
#         username = request.POST['email']
#         password = request.post['password']

#         usercred = authenticate(username=username, password=password)

#         if usercred is not None :
#             # log in the user
#             login(request, usercred)
#             # send them to the main page
#             return render(request, 'kidneyfoundation/index.html')

#         else :

#             messages.error(request, "Sorry, we couldn't sign you in. \n(Bad credentials)")
#             return redirect('dashboard-index')

#     return render(request, 'kidneyfoundation/signin.html')


def homePageView(request) :
    email = request.session['email']
    if (email) :
        data = User.objects.get(email=email)
    else :
        data = None
    context = {
        "user" : data,
        "logged_in" : loggedIn(request)
    }
    return render(request, 'kidneyfoundation/home.html', context)


def aboutPageView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }
    return render(request, 'kidneyfoundation/about.html', context)


def dashboardPageView(request) :
    email = request.session['email']
    userdata = User.objects.get(email=email)

    entrydata_all = Entry.objects.get(email=email)

    dt = datetime.now()
    today = datetime.today()
    a_week_ago = today - timedelta(days=7)
    
    rolling_week_entries = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": [],
    }

    for entry in entrydata_all :
        if entry.date >= a_week_ago and entry.date <= today :
            day_of_week = str(entry.date.strftime('%A'))
            rolling_week_entries[day_of_week]
            

    



    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }

    return render(request, 'kidneyfoundation/dashboard.html', context)


def chart2PageView(request) :
    return render(request, 'kidneyfoundation/chart2.html')

def suggestPageView(request, data=None) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }
    return render(request, 'kidneyfoundation/suggest.html', context)

def loggedIn(request) :
    logged_in = False
    email = request.session['email']
    if (email) :
        logged_in = True
    
    return logged_in

def diaryPageView(request, data=None, status=0, fdcId=0) :
    
    context = {
        'foods' : data,
        'status' : status,
        'nutrientIds' : [1093, 1003, 1092, 1091],
        'breakfast' : Entry.objects.select_related('fdcId').filter(email=request.session['email'], meal_type='B'),
        'lunch' : Entry.objects.select_related('fdcId').filter(email=request.session['email'], meal_type='L'),
        'dinner' : Entry.objects.select_related('fdcId').filter(email=request.session['email'], meal_type='D'),
        'snacks' : Entry.objects.select_related('fdcId').filter(email=request.session['email'], meal_type='S'),
        'logged_in' : loggedIn(request)

    }
    return render(request, 'kidneyfoundation/diary.html', context)

def findFood(request) :
    if request.method == 'POST' :
        r = requests.api.get('https://api.nal.usda.gov/fdc/v1/foods/search?query=' + request.POST['search'] + '&api_key=lS71PofdvinARzkWGHodOv25a5wD9DlDIlxyj9sH')
        if r.status_code == 200 :
            json_data = json.loads(r.content)
            return diaryPageView(request, json_data['foods'], r.status_code)

def addFoodView(request) :
    if request.method == 'POST' :
        # Declare variables
        k_value = request.POST['k_value']
        na_value = request.POST['na_value']
        phos_value = request.POST['phos_value']
        protien_value = request.POST['protein_value']
        fat_value = request.POST['fat_value']
        carbs_value = request.POST['carbs_value']
        calories = request.POST['calories']
        serving_size = request.POST['serving_size']

        # Get user info
        user = User.objects.get(email=request.session['email'])

        # Create food and entry object
        food = Food()
        entry = Entry()

        # Basic object info
        food.fdcId = request.POST['fdcId']
        food.food_name = request.POST['food_name']
        entry.meal_type = request.POST['meal']
        entry.num_servings = request.POST['servings']
        entry.email = user
        entry.fdcId = food

        # Serving size and micronutrients
        if (serving_size) :
            food.serving_size = serving_size
            food.serving_size_unit = request.POST['serving_size_unit']
        else :
            food.serving_size = 0.0
            food.serving_size_unit = None

        if (k_value) :
            food.k_value = k_value
            entry.k_intake = k_value
        else :
            food.k_value = 0.0
            entry.k_intake = 0.0
        
        if (na_value) :
            food.na_value = na_value
            entry.na_intake = na_value
        else :
            food.na_value = 0.0
            entry.na_intake = 0.0

        if (phos_value) :
            food.phos_value = phos_value
            entry.phos_intake = phos_value
        else :
            food.phos_value = 0.0
            entry.phos_intake = 0.0

        if (protien_value) :
            food.protien_value = protien_value
            entry.protein_intake = protien_value
        else :
            food.protien_value = 0.0
            entry.protein_intake = 0.0

        if (fat_value) :
            food.fat_value = fat_value
            entry.fat_intake = fat_value
        else :
            food.fat_value = 0.0
            entry.fat_intake = 0.0

        if (carbs_value) :
            food.carbs_value = carbs_value
            entry.carb_intake = carbs_value
        else :
            food.carbs_value = 0.0
            entry.carb_intake = 0.0

        if (calories) :
            food.calories = calories
        else :
            food.calories = 0.0

        # Save data
        food.save()
        entry.save()

    return diaryPageView(request)

def showUserPageView(request) :
    data = User.objects.get(email=request.session['email'])

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }

    return render(request, 'kidneyfoundation/showUser.html', context)



def editUserPageView(request):
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }

    return render(request, 'kidneyfoundation/editUser.html', context)

def updateUserInfoView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }

    if request.method == 'POST' :
        email = request.POST[ 'email' ]

        user = User.objects.get(email=email)

        user.email = request.POST[ 'email' ]
        user.password = request.POST['password']
        user.first_name = request.POST[ 'first_name' ]
        user.last_name = request.POST[ 'last_name' ]
        user.birthday = request.POST[ 'birthday' ]
        user.height = request.POST[ 'height' ]
        user.weight = request.POST[ 'weight' ]
        user.gender = request.POST[ 'gender' ]
        # user.date_signed_up = request.POST[ 'date_signed_up' ]
        user.on_dialysis = request.POST[ 'on_dialysis' ]
        user.stage = request.POST[ 'stage' ]
        
        user.save()

    return showUserPageView(request)

def showLevelsPageView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }

    return render(request, 'kidneyfoundation/showLevels.html', context)



def editLevelsPageView(request):
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }

    return render(request, 'kidneyfoundation/editLevels.html', context)



def updateLevelsView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data,
        'logged_in' : loggedIn(request)
    }
    
    if request.method == 'POST' :
        email = request.POST[ 'email' ]

        user = User.objects.get(email=email)

        user.k_level = request.POST[ 'k_level' ]
        user.na_level = request.POST[ 'na_level' ]
        user.phos_level = request.POST[ 'phos_level' ]
        user.creatinine_level = request.POST[ 'creatinine_level' ]
        user.albumin_level = request.POST[ 'albumin_level' ]
        user.blood_sugar_level = request.POST[ 'blood_sugar_level' ]
        
        user.save()

    
    return render(request, 'kidneyfoundation/showLevels.html', context)
