from django.shortcuts import render, redirect, HttpResponse
from senatiweb.decorators import firebase_login_required
from django.core.files.storage import FileSystemStorage
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
        idPost = Post.addPost(author, action, content)
        if request.FILES:
            # Si hay archivos en la solicitud POST

            uploaded_file = request.FILES['media']
            fs = FileSystemStorage()
            typeMedia = 'img'

            if '.jpg' in uploaded_file.name or '.png' in uploaded_file.name:
                location = os.path.join('posts', idPost + '.jpg')        
                if fs.exists(location):
                    os.remove('media/posts/' + idPost + '.jpg')

            elif '.gif' in uploaded_file.name:
                location = os.path.join('posts', idPost + '.gif')        
                if fs.exists(location):
                    os.remove('media/posts/' + idPost + '.gif')
                    
            elif '.mp4' in uploaded_file.name:
                location = os.path.join('posts', idPost + '.mp4')        
                if fs.exists(location):
                    os.remove('media/posts/' + idPost + '.mp4')
                typeMedia = 'video'
            else:
                return redirect('home')  
            name = fs.save(location, uploaded_file)
            urlMedia = fs.url(name)
            Post.updatePost(idPost, content, urlMedia, typeMedia)

        return redirect('home')
    else: 
        return render(request, "post/post.html")

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

