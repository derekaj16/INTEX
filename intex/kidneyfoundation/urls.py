from django.urls import path
from .views import *

urlpatterns = [
    path("user/<str:email>", showUserPageView, name="showUser"),
    path("about/", aboutPageView, name="about"),
    path("chart/", chartPageView, name="chart"),
    path("suggest/", suggestPageView, name='suggest'),
    path("updateUser/", updateUserInfoView, name='updateUser'),
    path("addUser/", addUserPageView, name='addUser'),
    path('search', searchFoodView, name='search'),
    path('edit/<str:email>', editUserPageView, name='edit'),
    path('', indexPageView, name='dashboard-index'),
]