from django.urls import path
from . import views

urlpatterns = [
    path('/myhome', views.home),
    path('/myhome2', views.home),
]