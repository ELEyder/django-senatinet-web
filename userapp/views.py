from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
            # Cambiar Foto de perfil
            fs = FileSystemStorage()
            typeMedia = 'img'
            uploaded_file = request.FILES['avatar']

            if '.jpg' in uploaded_file.name:
                location = os.path.join('avatars', userLogin['id'] + '.jpg')
                if fs.exists(location):
                    os.remove('media/avatars/' + userLogin['id'] + '.jpg')
            elif '.gif' in uploaded_file.name:
                location = os.path.join('avatars', userLogin['id'] + '.gif')
                if fs.exists(location):
                    os.remove('media/avatars/' + userLogin['id'] + '.gif')
            else:
                return redirect('home')
            name = fs.save(location, uploaded_file)
            urlAvatar = fs.url(name)
            
            # Publicar sobre tu cambio de perfil
            author = userLogin['firstName'] + ' ' + userLogin['lastName']
            avatar = userLogin['urlAvatar']
            content = '¡He actualizado mi foto de perfil!'
            idPost = Post.addPost(author,userLogin['id'], userLogin['username'], avatar, content)
            if '.jpg' in uploaded_file.name:
                location = os.path.join('posts', userLogin['id'] + '.jpg')
                if fs.exists(location):
                    os.remove('media/posts/' + userLogin['id'] + '.jpg')
            elif '.gif' in uploaded_file.name:
                location = os.path.join('posts', userLogin['id'] + '.gif')
                if fs.exists(location):
                    os.remove('media/posts/' + userLogin['id'] + '.gif')
            else:
                return redirect('home')
            name = fs.save(location, uploaded_file)
            urlMedia = fs.url(name)
            Post.updatePost(idPost, content, urlMedia, 'img')
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
        friendData = DefaultUser.getUserById(i)
        friendsData.append(friendData)
    return render(request, "user/profile.html", {'userLogin' : userLogin , 'friendsData' : friendsData, 'userData' : userData, 'posts' : posts})



@login_required
def viewUser(request, username):
    userAuth = request.user
    userLogin = DefaultUser.getUserByUsername(userAuth.username)
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


@login_required
def friendRequest(request, idUser):
    userAuth = request.user
    userLogin = DefaultUser.getUserByUsername(userAuth.username)
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