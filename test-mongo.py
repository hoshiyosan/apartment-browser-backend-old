from pymongo import MongoClient
from datetime import datetime

mongo = MongoClient('mongodb://admin:admin@localhost:27017/')

db = mongo.apartment
db.apartments.insert_one({
    'title': 'Bel appartement 3 pièces',
    'url': 'https://google.fr/apartment',
    'saved_on': datetime.now()
})
