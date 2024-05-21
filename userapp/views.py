from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from senatiweb.decorators import firebase_login_required
from django.http import HttpResponse
from django.conf import settings
import os

from .models import DefaultUser
from senatiweb.models import Country
from postapp.models import Post


# Create your views here.
@firebase_login_required
def userConfiguration(request):
    idAuth = request.session.get('user_id')
    userLogin = DefaultUser.getUserById(idAuth)
    countries = Country.getCountries()

    if request.method == "POST":
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        address = request.POST['address']
        country = request.POST['country']
        phone = request.POST['phone']
        if request.FILES:
            avatar = request.FILES['avatar']
            rpta = DefaultUser.updateUser(idAuth, firstName, lastName, address, country, phone, avatar)
            author = idAuth
            action = 'ha actualizado su foto de perfil'
            content = ''
            if rpta == 1: Post.addPost(author,action,content, avatar)
        else:
            DefaultUser.updateUser(idAuth, firstName, lastName, address, country, phone)
        return redirect('home')
    else:
        return render(request, "user/configuration.html", { 'userLogin':userLogin ,  'countries':countries })


@firebase_login_required
def viewUser(request, username):
    idAuth = request.session.get('user_id')
    userLogin = DefaultUser.getUserById(idAuth)
    userData = DefaultUser.getUserByUsername(username)
    posts = Post.getPostsByAuthorId(userData['id'])
    for post in posts:
        if (userLogin['id'] in post['likesD']):
            post['likeStatus'] = 'active'
        else:
            post['likeStatus'] = 'inactive'
    friendsData = []
    for i in userData['friends']:
        friendData = DefaultUser.getUserById(i)
        friendsData.append(friendData)
    return render(request, "user/profile.html", {'userLogin' : userLogin , 'friendsData' : friendsData, 'userData' : userData, 'posts' : posts})


@firebase_login_required
def friendRequest(request, idUser):
    idAuth = request.session.get('user_id')
    userLogin = DefaultUser.getUserById(idAuth)
    futureFriend = DefaultUser.getUserById(idUser)
    if idUser in userLogin['friendRequestR']:
        DefaultUser.acceptFriendRequest(userLogin['id'], idUser)
        return HttpResponse("¡Ahora son amigos!")
    elif idUser in userLogin['friendRequestS']:
        DefaultUser.deleteFriendRequestR(userLogin['id'], idUser)
        return HttpResponse("¡Solicitud eliminada!")
    else:
        msg = DefaultUser.sendFriendRequest(userLogin['id'] ,idUser)
        return HttpResponse(msg)