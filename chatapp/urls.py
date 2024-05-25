from django.urls import path
from .views import *

urlpatterns = [
    path('', chat, name='chat'),
    path('<str:id>/messages/', chatMessages, name='chatMessages'),
    path('<str:id>/send/', sendMessage, name='sendMessage'),
]

