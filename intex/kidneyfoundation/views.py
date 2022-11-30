from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from kidneyfoundation.models import User # need to make model for this
from datetime import datetime

# Create your views here.
def indexPageView(request):
    context = {
    }
    return render(request, 'kidneyfoundation/index.html', context)

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
    user = User.objects.get(email=email)

    context = {
        "user": user
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
        user.first_name = request.POST[ 'last_name' ]
        user.last_name = request.POST[ 'first_name' ]
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

        
        user.save()

        return showUserPageView(request, user.email)
    else: 
        return render (request, 'kidneyfoundation/addUser.html')