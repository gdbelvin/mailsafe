# App Engine Datastore model, "webapp/main.py"
from django.db import models
from google.appengine.ext import db
import uuid

class UUIDProperty(models.CharProperty) :
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharProperty, self).pre_save(model_instance, add)

class Author(db.Model):
    name = db.TextProperty()

class Supporter(db.Model):
    name = db.TextProperty()
    email = db.TextProperty()
    phone = db.TextProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)

class Link(db.Model):
    link = db.GUIDProperty()
    content_id = db.IntegerProperty()
    supporter = db.IntegerProperty()
    compromised = db.BoolProperty()
