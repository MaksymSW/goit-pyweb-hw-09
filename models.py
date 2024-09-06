
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import *

import configparser


config = configparser.ConfigParser()
config.read('config.ini')


mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


connect(db_name, host=uri)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {'collection': 'authors'}


class Quote(Document):
    author = ReferenceField(Author, required=True, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=100))
    quote = StringField(unique=True)
    meta = {'collection': 'quotes'}
