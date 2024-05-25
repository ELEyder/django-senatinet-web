from firebase_admin import firestore

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
            chats.append(chat_data)
        return chats
    
    @staticmethod
    def getMessagesById(id):         
        messages_data = db.collection(f'chats/{id}/messages').stream()
        messages = []
        for message in messages_data:
            message_data = message.to_dict()
            messages.append(message_data)
        return messages
    
    @staticmethod
    def addMessage(id, author, content):
        date = firestore.SERVER_TIMESTAMP
        data = {
            'author' : author,
            'content' : content,
            'date' : date
        }
        db.collection(f'chats/{id}/messages').add(data)