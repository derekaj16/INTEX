from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from kidneyfoundation.models import * # need to make model for this
from datetime import datetime, timedelta, date
from decimal import Decimal
import pytz


# feet/inches to centimeters Function
def heightToInches(feet, inches) :
    cm = (float(feet) * 12) + float(inches)
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
        user.height = heightToInches(request.POST[ 'feet' ], request.POST['inches'])
        user.weight = request.POST[ 'weight' ]
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
        user.blood_pressure = request.POST[ 'blood_pressure' ]
        user.diabetes = request.POST[ 'diabetes' ]
        
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
                
                # Then go and render the homepage, passing the session variable as the value for the email key in a nameless dictionary
                return homePageView(request)
            else :
                isError = True

    return indexPageView(request, isError)

def LogoutView(request) :
    request.session['email'] = None
    return redirect(homePageView)

def homePageView(request) :
    data = None
    logged_in = False
    email = ''
    if 'email' in request.session :
        if not request.session['email'] == None :
            email = request.session['email']
            data = User.objects.get(email=email)
            logged_in = loggedIn(request)
        
    context = {
        "user" : data,
        "logged_in" : logged_in
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
    user = User.objects.get(email=email)

    # getting all the records from the entry table
    entrydata_all = Entry.objects.select_related('fdcId').filter(email=email)
    

    today = datetime.now(pytz.timezone('US/Mountain')).date()
    a_week_ago = today - timedelta(days=7)

    rolling_week_entries = {
        0: [], # today
        1: [], # yesterday
        2: [], # 2 days ago
        3: [], # 3 days ago
        4: [], # 4 days ago
        5: [], # 5 days ago
        6: [], # 6 days ago
    }

    # For every entry record in the Entry table
    for entry in entrydata_all :
        # if the current entry's date is within the previous week
        if entry.date >= a_week_ago and entry.date <= today :
            # Find out how many days ago that entry was
            days_ago = (today - entry.date)
            # Adding the entry object to the key that corresponds with how many days ago that entry was
            rolling_week_entries[days_ago.days].append(entry)


    # Creating a list to hold all of the days of the week over the past rolling week
    days_of_week = []
    for day in range(0,7) :
        days_of_week.append(datetime.strftime(today, '%a, %b %d'))
        today = today - timedelta(days=1)

    days_of_week.reverse()

    k_data = []
    na_data = []
    phos_data = []

    # for each day in the rolling_week_entries dictionary
    for day in rolling_week_entries :
        # for each entry in that day
        dayK_intake = 0
        dayNa_intake = 0
        dayPhos_intake = 0
        
        if len(rolling_week_entries[day]) > 0 :
            for entry in rolling_week_entries[day] :
                print('Day: ' + str(day) + '   ' + str(entry.date))
                # getting the intake for each nutrient by mutliplying the nutrient's value for the food in the entry by the number of servings
                entryK_intake = int(entry.fdcId.k_value * entry.num_servings)
                entryNa_intake = int(entry.fdcId.na_value * entry.num_servings)
                entryPhos_intake = int(entry.fdcId.phos_value * entry.num_servings)
                
        else :
            entryK_intake = 0
            entryNa_intake = 0
            entryPhos_intake = 0
                
            # adding the entry's intake to the total intake of that nutrient for that day
        dayK_intake += entryK_intake
        dayNa_intake += entryNa_intake
        dayPhos_intake += entryPhos_intake

        # add the intake (# servings * nutrient amount) for each nutrient for that day to the list corresponding with that nutrient
        k_data.append(dayK_intake)
        na_data.append(dayNa_intake)
        phos_data.append(dayPhos_intake)

        # get today's data
        todays_k_intake = k_data[0]
        todays_na_intake = na_data[0]
        todays_phos_intake = phos_data[0]
        
    if user.on_dialysis :
        recommended_k = 2000
        recommended_na = (750 + 2000) / 2 # the middle number (optimal) between 750-2000
        recommended_phos = (800 + 1000) / 2 # the middle number (optimal) between 800-1000

    elif user.stage in (3,4): 
        recommended_k = (2500 + 3000) / 2 # the middle number (optimal) between 2500-3000
        recommended_na = (1495 + 2300) / 2 # the middle number (optimal) between 1495-2300
        recommended_phos = (800 + 1000) / 2 # the middle number (optimal) between 800-1000
    else :
        recommended_k = 3500
        recommended_na = 2300
        recommended_phos = 3000

    todays_k_percent = (todays_k_intake / recommended_k) * 100
    todays_na_percent = (todays_na_intake / recommended_na) * 100
    todays_phos_percent = (todays_phos_intake / recommended_phos) * 100

    # reversing the lists so that the dashboard shows the days in chronological order (not backwards chronological which would have today on the left)
    k_data.reverse()
    na_data.reverse()
    phos_data.reverse()
    
    context = {
        "user" : user,
        "past_week_entries": rolling_week_entries,
        "days_of_week": days_of_week,
        'logged_in' : loggedIn(request),
        "todays_k_percent": todays_k_percent,
        "todays_na_percent": todays_na_percent,
        "todays_phos_percent": todays_phos_percent,
        'k_data' : k_data,
        'na_data' : na_data,
        'phos_data' : phos_data
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

def diaryPageView(request, data=None, status=0, date=datetime.now(pytz.timezone('US/Mountain')).date()) :
    name = User.objects.get(email=request.session['email']).first_name
    context = {
        'name' : name,
        'foods' : data,
        'status' : status,
        'date' : date,
        'nutrientIds' : [1093, 1003, 1092, 1091],
        'breakfast' : Entry.objects.select_related('fdcId', 'email').filter(email=request.session['email'], meal_type='B', date=date),
        'lunch' : Entry.objects.select_related('fdcId', 'email').filter(email=request.session['email'], meal_type='L', date=date),
        'dinner' : Entry.objects.select_related('fdcId', 'email').filter(email=request.session['email'], meal_type='D', date=date),
        'snacks' : Entry.objects.select_related('fdcId', 'email').filter(email=request.session['email'], meal_type='S', date=date),
        'logged_in' : loggedIn(request)

    }
    return render(request, 'kidneyfoundation/diary.html', context)

def changeDate(request, date, forward) :
    newDate = datetime.strptime(date, '%Y-%m-%d')
    if forward == 'True' :
        newDate = newDate + timedelta(days=1)
    else :
        newDate = newDate - timedelta(days=1)

    return diaryPageView(request, date=newDate.date())

def findFood(request, date) :
    newDate = datetime.strptime(date, '%Y-%m-%d')
    if request.method == 'POST' :
        r = requests.api.get('https://api.nal.usda.gov/fdc/v1/foods/search?query=' + request.POST['search'] + '&api_key=lS71PofdvinARzkWGHodOv25a5wD9DlDIlxyj9sH')
        if r.status_code == 200 :
            json_data = json.loads(r.content)
            return diaryPageView(request, json_data['foods'], r.status_code, date=newDate.date())


def addFoodView(request) :
    if request.method == 'POST' :
        user = User.objects.get(email=request.session['email']) # Get user info
        entry = Entry() # Create entry
        entry.email = user
        date = request.POST['date']
        newDate = datetime.strptime(date, '%b. %d, %Y')
        entry.date = newDate
        entry.time = request.POST['time'] 

        # Declare variables
        k_value = request.POST['k_value']
        na_value = request.POST['na_value']
        phos_value = request.POST['phos_value']
        protien_value = request.POST['protein_value']
        fat_value = request.POST['fat_value']
        carbs_value = request.POST['carbs_value']
        calories = request.POST['calories']
        serving_size = request.POST['serving_size']
        servings = request.POST['servings']

        existingFood = Food.objects.filter(fdcId=request.POST['fdcId'])
        entry.num_servings = servings
        entry.meal_type = request.POST['meal']
        
        if  len(existingFood) > 0 : # Check if food is already inside database
            food = Food.objects.get(fdcId=request.POST['fdcId'])
            entry.fdcId = food

        else :
            # Create food and entry object
            food = Food()

            # Basic object info
            food.fdcId = request.POST['fdcId']
            food.food_name = request.POST['food_name']
            entry.fdcId = food

            # Serving size and micronutrients
            if (serving_size) :
                food.serving_size = serving_size
                food.serving_size_unit = request.POST['serving_size_unit']
            else :
                food.serving_size = 1.0
                food.serving_size_unit = None

            if (k_value) :
                food.k_value = float(k_value) * float(servings)
            else :
                food.k_value = 0.0
            
            if (na_value) :
                food.na_value = float(na_value) * float(servings)
            else :
                food.na_value = 0.0

            if (phos_value) :
                food.phos_value = float(phos_value) * float(servings)
            else :
                food.phos_value = 0.0

            if (protien_value) :
                food.protien_value = float(protien_value) * float(servings)
            else :
                food.protien_value = 0.0

            if (fat_value) :
                food.fat_value = float(fat_value) * float(servings)
            else :
                food.fat_value = 0.0

            if (carbs_value) :
                food.carbs_value = float(carbs_value) * float(servings)
            else :
                food.carbs_value = 0.0

            if (calories) :
                food.calories = float(calories) * float(servings)
            else :
                food.calories = 0.0

            # Save data
            food.save()
        
        entry.save()

    return diaryPageView(request, date=newDate.date())

def deleteFood(request, fdcId, email, date, time) :
    entry = Entry.objects.get(fdcId=fdcId, date=date, email=email, time=time)
    entry.delete()

    newDate = datetime.strptime(date, '%Y-%m-%d')


    return diaryPageView(request, date=newDate.date())

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
        user.on_dialysis = request.POST[ 'on_dialysis' ]
        user.stage = request.POST[ 'stage' ]
        user.blood_pressure = request.POST[ 'blood_pressure' ]
        user.diabetes = request.POST[ 'diabetes' ]
        
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
