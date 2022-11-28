from django.urls import path
from . import views
from .views import aboutPageView
from .views import showUserPageView
from .views import updateUserPageView
from .views import addUserPageView

urlpatterns = [
    path("user/<int:user_id>", showUserPageView, name="user"),
    path("about/", aboutPageView, name="about"),
    path("updateUser/", updateUserPageView, name='updateUser'),
    path("addUser/", addUserPageView, name='addUser'),
    path('', views.indexPageView, name='dashboard-index'),
]