from django.shortcuts import render
from django.http import HttpResponse
from kidneyfoundation.models import User # need to make model for this

# Create your views here.
def indexPageView(request):
    context = {
    }
    return render(request, 'kidneyfoundation/index.html', context)


def aboutPageView(request) :
    return render(request, 'kidneyfoundation/about.html')

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