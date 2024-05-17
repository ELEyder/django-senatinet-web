# from django.db import models
from django.conf import settings
from datetime import datetime
from firebase_admin import firestore
from shutil import copy

import os

db = firestore.client()

class DefaultUser():
    # Trae todos los usuarios
    @staticmethod
    def getUsers():
        users_ref = db.collection('users')
        users_docs = users_ref.get()
        users_data = []
        for doc in users_docs:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users_data.append(user_data)
        return users_data;
    # Trae todos los usuarios menos el logueado mediante su id
    @staticmethod
    def getUsersById(user_id):
        users_ref = db.collection('users')
        users_docs = users_ref.get()
        users_data = []
        for doc in users_docs:
            if doc.id == user_id:
                continue
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users_data.append(user_data)
        return users_data;
    
    # Trae un usuario por su id
    @staticmethod
    def getUserById(user_id):
        user_ref = db.collection('users').document(user_id)
        try:
            user_doc = user_ref.get().to_dict()
            user_doc['id'] = user_id
            return user_doc
        except NotFound:
            return None

    # Trae un usuario por su username
    @staticmethod
    def getUserByUsername(username):
        users_ref = db.collection('users')
        users_docs = users_ref.get()
        for doc in users_docs:
            user_data = doc.to_dict();
            user_data['id'] = doc.id
            if user_data['username'] == username:
                return user_data
        return 0;

    # Añade un usuario
    @staticmethod
    def addUser(id, userName, firstName, lastName, email, password):
        dt = datetime.now()

        data = {
            'address': 'Sin especificar',
            'country': 'Sin especificar',
            'email': email,
            'firstName': firstName,
            'firstRegistration': dt,
            'friendRequestR': [],
            'friendRequestS': [],
            'friends': [],
            'lastAccess': dt,
            'lastName': lastName,
            'nicknames' : [userName],
            'number': 'Sin registros',
            'password': password,
            'state': 'Desconectado',
            'studies': [],
            'urlAvatar': '/media/avatars/0.jpg',
            'username': userName,
            'works': [],
        }
        doc_ref = db.collection('users').document(id)
        doc_ref.set(data)
        ruta_original = os.path.join(settings.MEDIA_ROOT, 'avatars', '0.jpg')
        nueva_ruta = os.path.join(settings.MEDIA_ROOT, 'avatars', id + '.jpg')
        doc_ref.update({
            'urlAvatar' : '/media/avatars/' + id + '.jpg'
        })
        copy(ruta_original, nueva_ruta)

    def updateUser(id_user, address, country, email, firstName, lastName, number, urlAvatar):
        usuario_ref = db.collection("users").document(id_user)
        data = {
            'address': address,
            'country': country,
            'email': email,
            'firstName': firstName,
            'lastName': lastName,
            'number': number,
            'urlAvatar': urlAvatar
        }
        usuario_ref.update(data)

    @staticmethod
    def deleteFriendRequestR(idUser, idDelete):
        user_ref = db.collection("users").document(idUser)
        user_ref.update({
            'friendRequestR': firestore.ArrayRemove([idDelete])
        })

    @staticmethod
    def acceptFriendRequest(idfriend1, idfriend2):
        friend1 = db.collection("users").document(idfriend1)
        friend2 = db.collection("users").document(idfriend2)
        friend1.update({
            'friendRequestR': firestore.ArrayRemove([idfriend2]),
            'friendRequestS': firestore.ArrayRemove([idfriend2]),
            'friends': firestore.ArrayUnion([idfriend2])

        })
        friend2.update({
            'friendRequestR': firestore.ArrayRemove([idfriend1]),
            'friendRequestS': firestore.ArrayRemove([idfriend1]),
            'friends': firestore.ArrayUnion([idfriend1])
        })

    
    @staticmethod
    def sendFriendRequest(idSend, idReceive):
        send = db.collection("users").document(idSend)
        receive = db.collection("users").document(idReceive)
        doc = send.get()
        sendData = doc.to_dict()
        sendFriends = sendData.get('friends')
        sendFriendRequestR = sendData.get('friendRequestR')
        if idReceive in sendFriends:
            return 'Ellos ya son amigos'
        if idReceive in sendFriendRequestR:
            cls.acceptFriendRequest(idSend, idReceive)
            return 'Ahora son amigos'
        send.update({
            'friendRequestS': firestore.ArrayUnion([idReceive])
        })
        receive.update({
            'friendRequestR': firestore.ArrayUnion([idSend]),
        })
        return 'Solicitud Enviada'

