from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from senatiweb.decorators import firebase_login_required
from django.http import HttpResponse
from django.conf import settings
import os

from .models import DefaultUser
from postapp.models import Post


# Create your views here.
@firebase_login_required
def userConfiguration(request):
    idAuth = request.session.get('user_id')
    userLogin = DefaultUser.getUserById(idAuth)
    if request.method == "POST":
        if request.FILES:
            # Si hay archivos en la solicitud POST
            # Cambiar Foto de perfil
            fs = FileSystemStorage()
            typeMedia = 'img'
            uploaded_file = request.FILES['avatar']

            if '.jpg' in uploaded_file.name:
                location = os.path.join(settings.MEDIA_ROOT, 'avatars', userLogin['id'] + '.jpg')
                if os.path.exists(location):
                    os.remove(location)
            elif '.gif' in uploaded_file.name:
                location = os.path.join(settings.MEDIA_ROOT, 'avatars', userLogin['id'] + '.gif')
                if os.path.exists(location):
                    os.remove(location)
            else:
                return redirect('home')
            name = fs.save(location, uploaded_file)
            urlAvatar = fs.url(name)
            
            # Publicar sobre tu cambio de perfil
            author = userLogin['id']
            action = 'ha actualizado su foto de perfil'
            content = ''
            idPost = Post.addPost(author, action, content)
            if '.jpg' in uploaded_file.name:
                location = os.path.join(settings.MEDIA_ROOT, 'posts', idPost + '.jpg')
                if os.path.exists(location):
                    os.remove(location)
            elif '.gif' in uploaded_file.name:
                location = os.path.join(settings.MEDIA_ROOT, 'posts', idPost + '.gif')
                if os.path.exists(location):
                    os.remove(location)
            else:
                return redirect('home')
            name = fs.save(location, uploaded_file)
            urlMedia = fs.url(name)
            Post.updatePost(idPost, content, urlMedia, 'img')
        else:
            urlAvatar = userLogin['urlAvatar']
        
        DefaultUser.updateUser(userLogin['id'], request.POST['address'], request.POST['country'], request.POST['firstName'], request.POST['lastName'], request.POST['number'], urlAvatar)
        return redirect('home')
    else:
        return render(request, "user/configuration.html", { 'userLogin':userLogin})


@firebase_login_required
def viewProfile(request):
    idAuth = request.session.get('user_id')
    userLogin = DefaultUser.getUserById(idAuth)
    userData = DefaultUser.getUserByUsername(userLogin['username'])
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