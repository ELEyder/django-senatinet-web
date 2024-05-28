from firebase_admin import firestore
import os
from django.core.files.storage import FileSystemStorage

from django.conf import settings

db = firestore.client()

# Create your models here.
class Chat():
    @staticmethod
    def getChatsById(id):
        chats_data = db.collection('chats').where('members', 'array_contains', id).stream()
        chats = []
        for chat in chats_data:
            chat_data = chat.to_dict()
            chat_data['id'] = chat.id
            if len(chat_data['members']) == 2:
                chat_data['sender'] = id
                if chat_data['members'][0] == id:
                    receiverId = chat_data['members'][1]
                else:
                    receiverId = chat_data['members'][0]
                receiver = db.collection('users').document(receiverId).get().to_dict()
                chat_data['receiver'] = receiverId
                chat_data['receiverUsername'] = receiver['username']
                chat_data['receiverFirstName'] = receiver['firstName']
                chat_data['receiverLastName'] = receiver['lastName']
                chat_data['receiverUrlAvatar'] = receiver['urlAvatar']
            chats.append(chat_data)
        return chats
    
    @staticmethod
    def getMessagesById(id):         
        messages_data = db.collection(f'chats/{id}/messages').order_by('date', direction=firestore.Query.DESCENDING).stream()
        messages = []
        for message in messages_data:
            message_data = message.to_dict()
            messages.append(message_data)
        return messages
    
    @staticmethod
    def addMessage(id, author, content, media=None):
        date = firestore.SERVER_TIMESTAMP
        data = {
            'author' : author,
            'content' : content,
            'date' : date
        }
        ref = db.collection(f'chats/{id}/messages').add(data)
        idMessage = ref[1].id
        doc = db.collection(f'chats/{id}/messages').document(idMessage)
        if (media != None):
            fs = FileSystemStorage()
            typeMedia = 'img'
            if 'image/jpeg' in media.content_type:
                location = os.path.join(settings.MEDIA_ROOT, 'chats',id, idMessage + '.jpg')
            elif 'image/gif' in media.content_type:
                location = os.path.join(settings.MEDIA_ROOT, 'chats',id, idMessage + '.gif')
            elif 'video/mp4' in  media.content_type:
                location = os.path.join(settings.MEDIA_ROOT, 'chats',id, idMessage + '.mp4')
                typeMedia = 'video'
            else:
                return
            name = fs.save(location, media)
            urlMedia = fs.url(name)
            data = {
                'urlMedia': urlMedia,
                'typeMedia': typeMedia,
            }
            doc.update(data)
        
    @staticmethod
    def addChat(members):
        chat_temp = []
        for member in members:
            user = db.collection('users').document(member).get().to_dict()
            chat_temp.append(user['chats'])
        for id in chat_temp[0]:
            if id in chat_temp[1]:
                return {
                    'response' : False,
                    'idchat' : id
                }
        data = {
            'members' : members,
        }
        chat_ref = db.collection('chats').add(data)
        idChat = chat_ref[1].id
        for member in members:
            db.collection('users').document(member).update({
            'chats' : firestore.ArrayUnion([idChat])
        })
        return {
            'response' : True,
            'idchat' : idChat
        }
        