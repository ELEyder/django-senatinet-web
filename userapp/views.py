from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import os

from .models import DefaultUser
from postapp.models import Post


# Create your views here.
@login_required
def userConfiguration(request):
    userAuth = request.user
    userLogin = DefaultUser.getUserByUsername(userAuth.username)
    if request.method == "POST":
        userAuth.first_name = request.POST['firstName']
        userAuth.last_name = request.POST['lastName']
        userAuth.email = request.POST['email']
        userAuth.save()
        if request.FILES:
            # Si hay archivos en la solicitud POST
            uploaded_file = request.FILES['avatar']
            location = os.path.join('avatars', userLogin['id'] + '.jpg')
            fs = FileSystemStorage()
            if fs.exists(location):
                os.remove('media/avatars/' + userLogin['id'] + '.jpg')
            name = fs.save(location, uploaded_file)
            urlAvatar = fs.url(name)
        else:
            urlAvatar = userLogin['urlAvatar']
        
        DefaultUser.updateUser(userLogin['id'], request.POST['address'], request.POST['country'], request.POST['email'], request.POST['firstName'], request.POST['lastName'], request.POST['number'], urlAvatar)
        return redirect('home')
    else:
        return render(request, "user/configuration.html", { 'userLogin':userLogin})


@login_required
def viewProfile(request):
    userAuth = request.user
    userLogin = DefaultUser.getUserByUsername(userAuth.username)
    userData = DefaultUser.getUserByUsername(userAuth.username)
    posts = Post.getPostsByAuthorId(userData['id'])
    for post in posts:
        if (userLogin['id'] in post['likesD']):
            post['likeStatus'] = 'active'
        else:
            post['likeStatus'] = 'inactive'
    friendsData = []
    for i in userLogin['friends']:
        friendData = DefaultUser.getUserByUsername(i)
        friendsData.append(friendData)
    return render(request, "user/profile.html", {'userLogin' : userLogin , 'friendsData' : friendsData, 'userData' : userData, 'posts' : posts})



@login_required
def viewUser(request, username):
    userAuth = request.user
    userLogin = DefaultUser.getUserByUsername(userAuth.username)
    userData = DefaultUser.getUserByUsername(username)
    friendsData = []
    for i in userData['friends']:
        friendData = DefaultUser.getUserByUsername(i)
        friendsData.append(friendData)
    return render(request, "user/profile.html", {'userLogin' : userLogin , 'friendsData' : friendsData, 'userData' : userData})