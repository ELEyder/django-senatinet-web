from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


from postapp.models import Post
from userapp.models import DefaultUser
import os
# Create your views here.
@login_required
def postear(request):
    userAuth = request.user
    userLogin = DefaultUser.getUserByUsername(userAuth.username)
    if request.method == "POST":
        author = userLogin['firstName'] + ' ' + userLogin['lastName']
        avatar = userLogin['urlAvatar']
        content = request.POST['content']
        idPost = Post.addPost(author,userLogin['id'], userLogin['username'], avatar, content)
        if request.FILES:
            # Si hay archivos en la solicitud POST

            uploaded_file = request.FILES['media']
            fs = FileSystemStorage()
            typeMedia = 'img'

            if '.jpg' in uploaded_file.name:
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

@login_required
def like(request, id_post):
    username = request.user.username
    post = Post.getPostById(id_post)
    user = DefaultUser.getUserByUsername(username)
    if (user['id'] in post['likesD']):
        likes = int(post['likes']) - 1
        Post.updateLike(id_post, user['id'], likes, -1)
        return HttpResponse("¡Publicación unliked!")

    else:
        likes = int(post['likes']) + 1
        Post.updateLike(id_post, user['id'], likes, 1)
        return HttpResponse("¡Publicación liked!")

