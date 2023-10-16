from mongoengine import Document, DateTimeField, StringField
from datetime import datetime
from bson.objectid import ObjectId

def _create_object_id():
    return str(ObjectId())

class User(Document):
    dateCreated = DateTimeField(default=datetime.utcnow)
    mongo_id = StringField(required=True, primary_key=True, default=_create_object_id())
    keycloak_id = StringField(required=True)
    firstName = StringField(required=True)
    lastName = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=False)
