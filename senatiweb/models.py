# from django.db import models
from django.conf import settings
from datetime import datetime
from firebase_admin import firestore
from shutil import copy
from django.core.files.storage import FileSystemStorage

import os

db = firestore.client()

class Country():

    @staticmethod
    def getCountries():
        countries_docs = db.collection("countries").order_by("name", direction=firestore.Query.ASCENDING).get()
        countries = []
        for doc in countries_docs:
            country = doc.to_dict()
            country['id'] = doc.id
            countries.append(country)
        return countries