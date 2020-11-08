from flask_cors import CORS
from pymongo import MongoClient
from .settings import MONGODB_DATABASE_URL

cors = CORS()
db = MongoClient(MONGODB_DATABASE_URL).apartment
