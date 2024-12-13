from pymongo import MongoClient

MONGO_URI = "mongodb+srv://username:password@speech-therapy-new.qbvbh.mongodb.net/?retryWrites=true&w=majority"


client = MongoClient(MONGO_URI)
db = client['speech_therapy_app']
users_collection = db['users']
