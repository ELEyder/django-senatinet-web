from django.http import JsonResponse
from django.shortcuts import render
from senatiweb.decorators import firebase_login_required
from userapp.models import DefaultUser
from chatapp.models import Chat
import json
# Create your views here.
@firebase_login_required
def chat(request):
    userLogin = DefaultUser.getUserById(request.session.get('user_id')) 
    return render(request, "chat/chats.html", {'userLogin' : userLogin})
    
def getChats(request):
    chats = Chat.getChatsById(request.session.get('user_id'))
    return JsonResponse({'chats': chats})
    

@firebase_login_required
def chatMessages(request, id):
    messages = Chat.getMessagesById(id)
    return JsonResponse({'messages': messages})

@firebase_login_required
def sendMessage(request, id):
    if request.method == 'POST':
        message_data = json.loads(request.body)
        author = request.session.get('user_id')
        content = message_data.get('content')
        Chat.addMessage(id, author, content)
        return JsonResponse({'messages': 'susefull'})
    return JsonResponse({'messages': 'ERRORRRR'})
    
@firebase_login_required
def addChat(request):
    if request.method == 'POST':
        message_data = json.loads(request.body)
        friend = message_data.get('friend')
        members = [request.session.get('user_id'), friend]
        response = Chat.addChat(members)
        return JsonResponse(response)
    return JsonResponse({'response': 'ERRORRRR'})
    