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

@firebase_login_required
def getChats(request):
    chats = Chat.getChatsById(request.session.get('user_id'))
    return JsonResponse({'chats': chats})

@firebase_login_required
def addChat(request):
    if request.method == 'POST':
        message_data = json.loads(request.body)
        friend = message_data.get('friend')
        members = [request.session.get('user_id'), friend]
        response = Chat.addChat(members)
        return JsonResponse(response)
    return JsonResponse({'response': 'ERRORRRR'})

@firebase_login_required
def getMessages(request):
    message_data = json.loads(request.body)
    id = message_data.get('id')
    messages = Chat.getMessagesById(id)
    return JsonResponse({
        'id': id,
        'messages': messages
        })

@firebase_login_required
def addMessages(request):
    if request.method == 'POST':
        id = request.POST.get('id').strip()
        author = request.session.get('user_id')
        content = request.POST.get('content').strip()
        media = request.FILES.get('media', None)
        if media == None and content == '':
            return JsonResponse({'messages': 'ERRORRRR'})
        Chat.addMessage(id, author, content, media)
        return JsonResponse({'messages': 'susefull'})
    return JsonResponse({'messages': 'NO GET, POST'})
    

    