from django.urls import path
from .views import *

urlpatterns = [
    path("addUser/", addUserPageView, name='addUser'),
    path("user/<str:email>", showUserPageView, name="showUser"),
    path('edit/<str:email>', editUserPageView, name='edit'),
    path("updateUser/", updateUserInfoView, name='updateUser'),

    path("about/", aboutPageView, name="about"),
    path("chart/", chartPageView, name="chart"),
    path("chart2/", chart2PageView, name="chart2"),
    path("suggest/", suggestPageView, name='suggest'),
    path('search', searchFoodView, name='search'),
    
    path('levels/<str:email>', showLevelsPageView, name='showLevels'),
    path('editLevels/<str:email>', editLevelsPageView, name='editLevels'),
    path("updateLevels/", updateLevelsView, name='updateLevels'),
    path('', indexPageView, name='dashboard-index'),
]