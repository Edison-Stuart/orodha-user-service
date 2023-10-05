from mongoengine import Document, DateTimeField, StringField
from datetime import datetime

class User(Document):
    dateCreated = DateTimeField(default=datetime.utcnow)
    firstName = StringField(required=True)
    lastName = StringField(required=True)
    username = StringField(required=True)
    keycloak_id = StringField(required=True)
    email = StringField(required=False)
