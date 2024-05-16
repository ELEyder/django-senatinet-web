"""
URL configuration for senatiweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *
from userapp.views import *
from postapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', index, name='home'),
    path('', index, name='home'),
    path('logout/', exit, name='exit'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', login, name='signup'),
    path('user/configuration', userConfiguration, name='userConfiguration'),
    path('user/profile', viewProfile, name='viewProfile'),
    path('user/@<str:username>', viewUser, name='viewUser'),
    path('postear/', postear, name='postear'),
    path('like/<str:id_post>/', like, name='like'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)