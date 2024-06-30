from django.urls import path
from .views import *

urlpatterns = [
    path('', chat, name='chat'),
    path('get/', getChats, name='getChats'),
    path('add/', addChat, name='addChat'),
    path('get/messages/', getMessages, name='getMessages'),
    path('add/messages/', addMessages, name='addMessages'),
]

