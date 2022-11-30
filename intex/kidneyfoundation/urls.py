from django.urls import path
from .views import *

urlpatterns = [
    # path('signup/', signupPageView, name='signup'),
    path("addUser/", addUserPageView, name='addUser'),
    path("user/", showUserPageView, name="showUser"),
    path('edit/', editUserPageView, name='edit'),
    path("updateUser/", updateUserInfoView, name='updateUser'),

    path("about/", aboutPageView, name="about"),
    path("dashboard/", dashboardPageView, name="dashboard"),
    path("chart2/", chart2PageView, name="chart2"),
    path("suggest/", suggestPageView, name='suggest'),
    path('search/', searchFoodView, name='search'),
    path('home/', homePageView, name='home'),
    
    path('levels/', showLevelsPageView, name='showLevels'),
    path('editLevels/', editLevelsPageView, name='editLevels'),
    path("updateLevels/", updateLevelsView, name='updateLevels'),
    
    path('login', LoginView, name='login'),
    path('logout', LogoutView, name='logout'),
    path('', indexPageView, name='index'),
]