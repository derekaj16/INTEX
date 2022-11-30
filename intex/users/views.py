from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def registerPageView(request) :
    form = UserCreationForm()
    

    return render(request, 'users/register.html', {'form': form})