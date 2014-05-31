# App Engine Datastore model, "webapp/main.py"
from django.db import models
from google.appengine.ext import db
import uuid

class UUIDProperty(db.StringProperty) :
    
    def __init__(self, *args, **kwargs):
        db.StringProperty.__init__(self, *args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(db.StringProperty, self).pre_save(model_instance, add)

class Author(db.Model):
    name = db.TextProperty()

class Supporter(db.Model):
    name = db.TextProperty()
    email = db.TextProperty()
    phone = db.TextProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)

class Content(db.Model):
    text = db.TextProperty()
    blob = db.BlobProperty()

class Link(db.Model):
    link = UUIDProperty()
    content = db.IntegerProperty()
    supporter = db.IntegerProperty()
    compromised = db.BooleanProperty()
