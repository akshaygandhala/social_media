from flask_login import UserMixin 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://traininglatrics2:eyBNCmy294K5Xipi@main.lab28gt.mongodb.net/?retryWrites=true&w=majority&appName=social" 
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.name = user_data['name']
        self.email = user_data['email']
        self.contact = user_data['contact']
        self.password = user_data['password']

    @staticmethod
    def get(user_id, client):
        user = client.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        return User(user)
