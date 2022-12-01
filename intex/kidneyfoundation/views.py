from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from kidneyfoundation.models import * # need to make model for this
from datetime import datetime, timedelta

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
                return redirect('home')
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

    # getting the current user's email from session storage
    email = request.session['email']

    # getting the object that has that email
    data = User.objects.get(email=email)

    # passing that user object's data to a dictionary so we can pass that to the page
    context = {
        "user" : data
    }
    return render(request, 'kidneyfoundation/home.html', context)


def aboutPageView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data
    }
    return render(request, 'kidneyfoundation/about.html', context)


def dashboardPageView(request) :
    email = request.session['email']
    userdata = User.objects.get(email=email)

    # getting all the records from the entry table
    entrydata_all = Entry.objects.get(email=email)

    dt = datetime.now()
    today = datetime.today()
    a_week_ago = today - timedelta(days=7)

    rolling_week_entries = {
        0: [], # today
        1: [], # yesterday
        2: [], # 2 days ago
        3: [], # 3 days ago
        4: [], # 4 days ago
        5: [], # 5 days ago
        6: [], # 6 days ago
        7: [], # 1 full week ago (if today is Wendesday, this is last Wednesday)
    }
    
    # For every entry record in the Entry table
    for entry in entrydata_all :
        # if the current entry's date is within the previous week
        if entry.date >= a_week_ago and entry.date <= today :
            # Find out how many days ago that entry was
            days_ago = timedelta(today) - timedelta(entry.date)
            # Adding the entry object to the key that corresponds with how many days ago that entry was
            rolling_week_entries[days_ago].append(entry)

    # Creating a list to hold all of the days of the week over the past rolling week
    days_of_week = []

    # For each day (key) in the rolling_week_entries table
    for day_number in rolling_week_entries:
        # get the number of days before the current day
        entry_day_of_week_date = rolling_week_entries[day_number][0].date

        # get the day of the week of the entries of the day ago thing
        day_of_week_name = str(entry_day_of_week_date.strftime('%A'))

        # appending that day of the week name to the list holding all of the names of the days of the week from the past rolling week
        days_of_week.append(day_of_week_name)


    context = {
        "user" : userdata,
        "past_week_entries": rolling_week_entries,
        "days_of_week": days_of_week,
    }

    return render(request, 'kidneyfoundation/dashboard.html', context)


def chart2PageView(request) :
    return render(request, 'kidneyfoundation/chart2.html')


def suggestPageView(request, data=None) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data
    }
    return render(request, 'kidneyfoundation/suggest.html', context)


def diaryPageView(request, data=None, status=0) :
    breakfast = 'hello'

    context = {
        'foods' : data,
        'status' : status,
        'nutrientIds' : [1093, 1003, 1092, 1091],
        'breakfast': breakfast
    }
    return render(request, 'kidneyfoundation/diary.html', context)


def findFood(request) :
    if request.method == 'POST' :
        r = requests.api.get('https://api.nal.usda.gov/fdc/v1/foods/search?query=' + request.POST['search'] + '&api_key=lS71PofdvinARzkWGHodOv25a5wD9DlDIlxyj9sH')
        if r.status_code == 200 :
            json_data = json.loads(r.content)
            return diaryPageView(request, json_data['foods'], r.status_code)


def addFoodView(request) :
    return diaryPageView(request)


def showUserPageView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data
    }

    return render(request, 'kidneyfoundation/showUser.html', context)


def editUserPageView(request):
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data
    }

    return render(request, 'kidneyfoundation/editUser.html', context)


def updateUserInfoView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data
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
        "user" : data
    }

    return render(request, 'kidneyfoundation/showLevels.html', context)



def editLevelsPageView(request):
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data
    }

    return render(request, 'kidneyfoundation/editLevels.html', context)



def updateLevelsView(request) :
    email = request.session['email']
    data = User.objects.get(email=email)

    context = {
        "user" : data
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
