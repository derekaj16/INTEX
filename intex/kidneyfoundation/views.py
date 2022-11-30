from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from kidneyfoundation.models import User # need to make model for this
from datetime import datetime

# Create your views here.
def indexPageView(request) :
    return render(request, 'kidneyfoundation/index.html')


def signupPageView(request) :
    return render(request, 'kidneyfoundation/signup.html')


def LoginView(request) :

    if request.method == 'POST' :
        username = request.POST['email']
        password = request.POST['password']

        allUsers = User.objects.all()

        for current_user in allUsers :
            if username == current_user.email :
                user = User.objects.get(email=username)

            return render(request, 'kidneyfoundation/home.html', {'email': user.email})

        return redirect('index')


def homePageView(request, email) :
    return render(request, 'kidneyfoundation/home.html', {'email': email})

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


def aboutPageView(request) :
    return render(request, 'kidneyfoundation/about.html')

def chartPageView(request) :
    return render(request, 'kidneyfoundation/chart.html')

def suggestPageView(request, data=None) :
    context = {
        'data': data
    }
    return render(request, 'kidneyfoundation/suggest.html', context)

def searchFoodView(request) :
    if request.method == 'POST' :
        r = requests.api.get('https://api.nal.usda.gov/fdc/v1/foods/search?query=' + request.POST['search'] + '&pageSize=2&api_key=lS71PofdvinARzkWGHodOv25a5wD9DlDIlxyj9sH')
    if r.status_code == 200 :
        json_data = json.loads(r.content)
        if len(json_data['foods']) > 0 :
            return suggestPageView(request, json_data['foods'])
        else :
            return suggestPageView(request, 'Your search for ' + request.POST['search'] + ' was not found :/')

def showUserPageView(request, email) :
    data = User.objects.get(email=email)

    context = {
        "user": data
    }

    return render(request, 'kidneyfoundation/showUser.html', context)



def editUserPageView(request, email):
    data = User.objects.get(email=email)
    
    context = {
        "user" : data
    }

    return render(request, 'kidneyfoundation/editUser.html', context)

def updateUserInfoView(request) :
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

    return showUserPageView(request, user.email)

def addUserPageView(request) :
    if request.method == 'POST' :
        user = User()

        user.email = request.POST[ 'email' ]
        user.first_name = request.POST[ 'last_name' ]
        user.last_name = request.POST[ 'first_name' ]
        user.birthday = request.POST[ 'birthday' ]
        user.height = request.POST[ 'height' ]
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

        
        # if User.objects.filter(email=email) :
        #     messages.error(request, "That username already exists. Please use a different username")


        user.save()

        # creates a django user???
        # myuser = User.objects.create_user(username, email, password)

        # creates a django user???
        # myuser.save()

        return showUserPageView(request, user.email)
    else: 
        return render (request, 'kidneyfoundation/addUser.html')




def showLevelsPageView(request, email) :
    data = User.objects.get(email=email)

    context = {
        "user": data
    }

    return render(request, 'kidneyfoundation/showLevels.html', context)



def editLevelsPageView(request, email):
    data = User.objects.get(email=email)
    
    context = {
        "user" : data
    }

    return render(request, 'kidneyfoundation/editLevels.html', context)



def updateLevelsView(request) :
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

    return showLevelsPageView(request, user.email)
