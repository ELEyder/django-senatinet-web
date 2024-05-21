from django.shortcuts import render, redirect
from userapp.models import DefaultUser
from postapp.models import Post
from .decorators import firebase_login_required
from firebase_admin import auth
from django.http import HttpResponse
import os
import pyrebase
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

firebase = pyrebase.initialize_app(firebase_config)

@firebase_login_required
def index(request):
    userLogin = DefaultUser.getUserById(request.session.get('user_id'))
    posts = Post.getPosts()
    users = DefaultUser.getUsersById(userLogin['id'])
    for post in posts:
        if (userLogin['id'] in post['likesD']):
            post['likeStatus'] = 'active'
        else:
            post['likeStatus'] = 'inactive'
    for userG in users:
        if (userLogin['id'] in userG['friendRequestR']):
            userG['fStatus'] = 'Cancel'
        elif (userLogin['id'] in userG['friendRequestS']):
            userG['fStatus'] = 'Accept'
        elif (userLogin['id'] in userG['friends']):
            userG['fStatus'] = 'View'
        else:
            userG['fStatus'] = 'Send'

        
    return render(request, "index.html", {'users':users, 'userLogin':userLogin, 'posts':posts})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        authentication = firebase.auth()
        try:
            user = authentication.sign_in_with_email_and_password(email, password)
            request.session['user_id'] = user['localId']
            return redirect('home')
        except:
            return HttpResponse("Credenciales incorrectas")

            
    return render(request, 'user/login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        username = request.POST['username']
        users = DefaultUser.getUsers()
        for user in users:
            if username == user['username']:
                return HttpResponse("Usuario ya existe")
        if request.POST['password1'] != request.POST['password2']:
            return HttpResponse("Contraseñas diferentes, vuelve a la página anterior, luego lo hago con js :)")
        try:
            user = auth.create_user(email = email, password = password)
            DefaultUser.addUser(
                id = user.uid,
                userName=request.POST['username'],
                firstName=request.POST['firstname'],
                lastName=request.POST['lastname'],
                email=request.POST['email'],
            )
            return HttpResponse("Usuario Creado")
        except:
            return HttpResponse("Error al crear usuario: Ya existe el correo registrado u otro error no relacionado conmigo:")

    return redirect('login')

def exit(request):
    request.session.flush()
    return redirect('login')





