from django.urls import path
from .views import *

urlpatterns = [
    path('', chat, name='chat'),
    path('<str:id>/messages/', chatMessages, name='chatMessages'),
    path('get/', getChats, name='getChats'),
    path('<str:id>/send/', sendMessage, name='sendMessage'),
    path('add/', addChat, name='addChat'),
]

