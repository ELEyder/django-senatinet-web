from django.urls import path
from .views import *

urlpatterns = [
    path('configuration/', userConfiguration, name='userConfiguration'),
    path('@<str:username>', viewUser, name='viewUser'),
    path('friendRequest/<str:idUser>', friendRequest, name='friendRequest'),
]