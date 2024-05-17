from django.db import models
from firebase_admin import firestore
from datetime import datetime

db = firestore.client()
# Create your models here.
class Post():
    @staticmethod
    def addPost(author, action, content):
        date = datetime.now()
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
        try:
            doc = db.collection('posts').add(data)
            return doc[1].id
        except Exception as e:
            print('Error al agregar el documento:', e)
            
    @staticmethod
    def getPosts():
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
        posts_docs = posts_ref.get()
        posts_data = []
        for doc in posts_docs:
            post_data = doc.to_dict()
            post_data['id'] = doc.id
            if post_data['idAuthor'] == author_id:
                posts_data.append(post_data)
        return posts_data
    
    @staticmethod
    def updatePost(id_post, content, urlMedia, typeMedia):
        post_ref = db.collection("posts").document(id_post)
        data = {
            'content': content,
            'urlMedia': urlMedia,
            'typeMedia': typeMedia,
        }
        post_ref.update(data)
    
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



