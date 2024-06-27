from firebase_admin import firestore

class Country():

    db = firestore.client()

    @staticmethod
    def getCountries():
        countries_docs = Country.db.collection("countries").order_by("name", direction=firestore.Query.ASCENDING).get()
        countries = []
        for doc in countries_docs:
            country = doc.to_dict()
            country['id'] = doc.id
            countries.append(country)
        return countries