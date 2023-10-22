"""Module which contains the definition for our User mongoengine Document."""
from mongoengine import Document, DateTimeField, StringField
from datetime import datetime


class User(Document):
    dateCreated = DateTimeField(default=datetime.utcnow)
    keycloak_id = StringField(required=True)
    firstName = StringField(required=True)
    lastName = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=False)
