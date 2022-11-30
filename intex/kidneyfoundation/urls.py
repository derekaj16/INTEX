from django.urls import path
from .views import *

urlpatterns = [
    path("addUser/", addUserPageView, name='addUser'),
    path("user/<str:email>", showUserPageView, name="showUser"),
    path('edit/<str:email>', editUserPageView, name='edit'),
    path("updateUser/", updateUserInfoView, name='updateUser'),
    path("about/", aboutPageView, name="about"),
    path("chart/", chartPageView, name="chart"),
    path("suggest/", suggestPageView, name='suggest'),
    path('diary', diaryPageView, name='diary'),
    path('find', findFood, name='find'),
    path('add', addFoodView, name='add'),
    path('levels/<str:email>', showLevelsPageView, name='showLevels'),
    path('editLevels/<str:email>', editLevelsPageView, name='editLevels'),
    path("updateLevels/", updateLevelsView, name='updateLevels'),
    path('', indexPageView, name='dashboard-index'),
]