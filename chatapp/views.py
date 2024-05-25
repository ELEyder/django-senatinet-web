from django.http import JsonResponse
from django.shortcuts import render
from senatiweb.decorators import firebase_login_required
from userapp.models import DefaultUser
from chatapp.models import Chat
import json
# Create your views here.
@firebase_login_required
def chat(request):
    idAuth = request.session.get('user_id')
    chats = Chat.getChatsById(idAuth)
    return render(request, "chat/chats.html", {'chats' : chats, 'idAuth' : idAuth})

@firebase_login_required
def chatMessages(request, id):
    messages = Chat.getMessagesById(id)
    return JsonResponse({'messages': messages})

def sendMessage(request, id):
    if request.method == 'POST':
        message_data = json.loads(request.body)
        author = message_data.get('author')
        content = message_data.get('content')
        Chat.addMessage(id, author, content)
        return JsonResponse({'messages': 'susefull'})
    return JsonResponse({'messages': 'ERRORRRR'})
    