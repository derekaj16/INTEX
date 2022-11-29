from django.urls import path
from .views import *

urlpatterns = [
    path("user/<int:user_id>", showUserPageView, name="user"),
    path("about/", aboutPageView, name="about"),
    path("chart/", chartPageView, name="chart"),
    path("suggest/", suggestPageView, name='suggest'),
    path("updateUser/", updateUserPageView, name='updateUser'),
    path("addUser/", addUserPageView, name='addUser'),
    path('search', searchFoodView, name='search'),
    path('', indexPageView, name='dashboard-index'),
]