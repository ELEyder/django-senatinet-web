from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from userapp.models import DefaultUser
from postapp.models import Post
import os

@login_required
def index(request):
    userAuth = request.user
    userLogin = DefaultUser.getUserByUsername(userAuth.username)
    posts = Post.getPosts()
    users = DefaultUser.getUsersById(userLogin['id'])
    for post in posts:
        if (userLogin['id'] in post['likesD']):
            post['likeStatus'] = 'active'
        else:
            post['likeStatus'] = 'inactive'
        
    return render(request, "index.html", {'users':users, 'userLogin':userLogin, 'posts':posts})

def login(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password1'],)
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.save()
            DefaultUser.addUser(
                userName=request.POST['username'],
                firstName=request.POST['firstname'],
                lastName=request.POST['lastname'],
                email=request.POST['email'],
                password=request.POST['password1'],
            )
            print("Usuario Guardado")
            return redirect('login')
        return render(request, "registration/login.html")
    else:
        return render(request, "index.html")

def exit(request):
    logout(request)
    return redirect('login')





