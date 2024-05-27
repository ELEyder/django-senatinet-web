from firebase_admin import firestore
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from datetime import datetime, timedelta
import pytz
from tzlocal import get_localzone
from dotenv import load_dotenv
load_dotenv()

db = firestore.client()

class Post():
    @staticmethod
    def addPost(author, action, content, media=None):
        fs = FileSystemStorage()
        date = firestore.SERVER_TIMESTAMP
        data = {
            'author': author,
            'action': action,
            'date' : date,
            'content': content,
            'urlMedia': '',
            'typeMedia': '',
            'likes': 0,
            'likesD': [],
            'comments': 0,
            'commentsD': [],
            'searchs': 0,
            'searchsD': [],
            'privacy' : "Público",
            'privacyD' : []
        }
        doc = db.collection('posts').add(data)
        id_post = doc[1].id
        doc = db.collection('posts').document(id_post)
        if media != None:
            typeMedia = 'img'
            if 'image/jpeg' in media.content_type:
                location = os.path.join(settings.MEDIA_ROOT, 'posts', id_post + '.jpg')
            elif 'image/gif' in media.content_type:
                location = os.path.join(settings.MEDIA_ROOT, 'posts', id_post + '.gif')
            elif 'video/mp4' in  media.content_type:
                location = os.path.join(settings.MEDIA_ROOT, 'posts', id_post + '.mp4')
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
        return
            
    @staticmethod
    def getPosts():
        posts_docs = db.collection('posts').order_by('date', direction=firestore.Query.DESCENDING).get()
        users_docs = db.collection('users').get()
        posts_data = []
        for doc in posts_docs:
            post_data = doc.to_dict()
            post_data['id'] = doc.id
            # Obtener la zona horaria local del usuario
            local_timezone = get_localzone()

            # Obtener la fecha y hora actuales en la zona horaria local del usuario
            now_local = datetime.now(local_timezone)

            # Obtener el desplazamiento horario de UTC para la zona horaria local del usuario
            utc_offset_hours = local_timezone.utcoffset(now_local)
            post_data['date'] = post_data['date'] + utc_offset_hours
            for docUser in users_docs:
                if docUser.id == post_data['author']:
                    data = docUser.to_dict()
                    post_data['authorName'] = data['firstName'] + ' ' + data['lastName']
                    post_data['authorUsername'] = data['username']
                    post_data['authorAvatar'] = data['urlAvatar']
            posts_data.append(post_data)
        return posts_data
    @staticmethod
    def getPostById(post_id):
        post_ref = db.collection('posts').document(post_id)
        try:
            post_doc = post_ref.get().to_dict()
            post_doc['id'] = post_id
            return post_doc
        except:
            return None
    
    @staticmethod
    def getPostsByAuthorId(author_id):
        posts_ref = db.collection('posts')
        users_ref = db.collection('users')
        posts_docs = posts_ref.get()
        users_docs = users_ref.get()
        posts_data = []
        for doc in posts_docs:
            post_data = doc.to_dict()
            for docUser in users_docs:
                if docUser.id == post_data['author']:
                    data = docUser.to_dict()
                    post_data['authorName'] = data['firstName'] + ' ' + data['lastName']
                    post_data['authorUsername'] = data['username']
                    post_data['authorAvatar'] = data['urlAvatar']
            post_data['id'] = doc.id
            if post_data['author'] == author_id:
                posts_data.append(post_data)
        return posts_data
    
    @staticmethod
    def updatePost(id_post, content, urlMedia, typeMedia):
        return None

    
    @staticmethod
    def updateLike(id_post, id_user, likes, state):
        post_ref = db.collection("posts").document(id_post)

        if state == 1:
            post_ref.update({
                'likesD': firestore.ArrayUnion([id_user])
            })
        else:
            post_ref.update({
                'likesD': firestore.ArrayRemove([id_user])
            })

        data = {
            'likes': likes,
        }
        post_ref.update(data)

    @staticmethod
    def addComment(id_post, id_user, content):
        date = firestore.SERVER_TIMESTAMP
        data = {
            'author': id_user,
            'content': content,
            'date' : date,
            'post': id_post,
            'typeMedia': '',
            'urlMedia': '',
            'likes': 0,
            'likesD': []
        }
        db.collection('comments').add(data)
    
    @staticmethod
    def getComments(id_post):
        com_ref = db.collection('comments').where("post", "==", id_post)
        com_docs = com_ref.get()
        users_docs = db.collection('users').get()
        coms_data = []
        for doc in com_docs:
            com_data = doc.to_dict()
            com_data['id'] = doc.id
            for docUser in users_docs:
                if docUser.id == com_data['author']:
                    data = docUser.to_dict()
                    com_data['authorName'] = data['firstName'] + ' ' + data['lastName']
                    com_data['authorUsername'] = data['username']
                    com_data['authorAvatar'] = data['urlAvatar']
            coms_data.append(com_data)
        return coms_data
