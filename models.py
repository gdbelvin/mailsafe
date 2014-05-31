# App Engine Datastore model, "webapp/main.py"
from django.db import models
from google.appengine.ext import ndb
import uuid

class UUIDProperty(ndb.StringProperty) :
    
    def __init__(self, *args, **kwargs):
        ndb.StringProperty.__init__(self, *args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(ndb.StringProperty, self).pre_save(model_instance, add)

class Author(ndb.Model):
    name = ndb.TextProperty()

<<<<<<< Updated upstream
class Supporter(ndb.Model):
    name = ndb.TextProperty()
    email = ndb.TextProperty()
    phone = ndb.TextProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)
=======
class Supporter(db.Model):
    name = db.TextProperty()
    email = db.EmailProperty()
    phone = db.PhoneNumberProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)
>>>>>>> Stashed changes

class Content(ndb.Model):
    blob = ndb.BlobProperty()
    text = ndb.TextProperty()

class Link(ndb.Model):
    link = UUIDProperty()
<<<<<<< Updated upstream
    supporter_id = ndb.IntegerProperty()
    content_id = ndb.IntegerProperty()
    compromised = ndb.BooleanProperty()
=======
    supporter = db.ReferenceProperty(Supporter)
    supporter_id = db.IntegerProperty()
    content = db.ReferenceProperty(Content)
    content_id = db.IntegerProperty()
    compromised = db.BooleanProperty()
>>>>>>> Stashed changes
