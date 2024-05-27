from django.shortcuts import render, redirect, HttpResponse
from senatiweb.decorators import firebase_login_required
from django.http import HttpResponse
from postapp.models import Post
from userapp.models import DefaultUser
import os
# Create your views here.
@firebase_login_required
def postear(request):
    idAuth = request.session.get('user_id')
    userLogin = DefaultUser.getUserById(idAuth)
    if request.method == "POST":
        author = userLogin['id']
        content = request.POST['content']
        action = ''
        if request.FILES:
            media = request.FILES['media']
            Post.addPost(author, action, content, media)
            return redirect('home')
        Post.addPost(author, action, content)
        return redirect('home')
    return redirect('home')

@firebase_login_required
def like(request, id_post):
    idAuth = request.session.get('user_id')
    userLogin = DefaultUser.getUserById(idAuth)
    post = Post.getPostById(id_post)
    if (userLogin['id'] in post['likesD']):
        likes = int(post['likes']) - 1
        Post.updateLike(id_post, userLogin['id'], likes, -1)
        return HttpResponse("¡Publicación unliked!")

    else:
        likes = int(post['likes']) + 1
        Post.updateLike(id_post, userLogin['id'], likes, 1)
        return HttpResponse("¡Publicación liked!")

@firebase_login_required
def comment(request):
    if request.method == "POST":
        idAuth = request.session.get('user_id')
        content = request.POST['comment']
        idPost = request.POST['idPost']
        Post.addComment(idPost, idAuth, content)
        return redirect('home')
    return redirect('home')

