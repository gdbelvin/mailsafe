from django.db import models
from google.appengine.ext import ndb
import uuid

class UUIDProperty(ndb.StringProperty) :
    
    def __init__(self, *args, **kwargs):
        ndb.StringProperty.__init__(self, *args, **kwargs)
    
    def _pre_put_hook(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(ndb.StringProperty, self)._pre_put_hook()

class Author(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()

class Supporter(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    of = ndb.KeyProperty(kind=Author, repeated=True)
    tags = ndb.StringProperty(repeated=True)
    date_created = ndb.DateTimeProperty(auto_now_add=True)

class Content(ndb.Model):
    blob = ndb.BlobProperty()
    text = ndb.TextProperty()
    author = ndb.KeyProperty(kind=Author)

class Link(ndb.Model):
    link = UUIDProperty()
    uuid = ndb.StringProperty()
    supporter = ndb.KeyProperty(kind=Supporter)
    content = ndb.KeyProperty(kind=Content)
    compromised = ndb.BooleanProperty()

    content_id = ndb.IntegerProperty()
    supporter_id = ndb.IntegerProperty()
