from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from kidneyfoundation.models import User # need to make model for this

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

def showUserPageView(request, user_id) :
    user = User.objects.get(id=user_id)

    context = {
        "user": user
    }

    return render(request, 'kidneyfoundation/showUser.html', context)

def updateUserPageView(request) :
    if request.method == 'POST' :
        user_id = request.POST[ 'user_id' ]

        user = User.objects.get(id=user_id)

        user.first_name = request.POST[ 'last_name' ]
        user.last_name = request.POST[ 'first_name' ]
        user.user_name = request.POST[ 'user_name' ]
        user.password = request.POST[ 'password' ]
        user.email = request.POST[ 'email' ]
        user.phone = request.POST[ 'phone' ]
        
        user.save()

    return showUserPageView(request)

def addUserPageView(request) :
    if request.method == 'POST' :
        user = User()

        user.first_name = request.POST[ 'last_name' ]
        user.last_name = request.POST[ 'first_name' ]
        user.user_name = request.POST[ 'user_name' ]
        user.password = request.POST[ 'password' ]
        user.email = request.POST[ 'email' ]
        user.phone = request.POST[ 'phone' ]
        
        user.save()

        return showUserPageView(request)
    else: 
        return render (request, 'kidneyfoundation/addUser.html')