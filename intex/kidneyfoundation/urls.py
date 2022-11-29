from django.urls import path
from .views import indexPageView
from .views import aboutPageView
from .views import showUserPageView
from .views import updateUserPageView
from .views import addUserPageView
from .views import chartPageView

urlpatterns = [
    path("user/<int:user_id>", showUserPageView, name="user"),
    path("about/", aboutPageView, name="about"),
    path("chart/", chartPageView, name="chart"),
    path("updateUser/", updateUserPageView, name='updateUser'),
    path("addUser/", addUserPageView, name='addUser'),
    path('', indexPageView, name='dashboard-index'),
]