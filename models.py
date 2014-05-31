from django.db import models
from google.appengine.ext import ndb
import uuid

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
    uuid = ndb.StringProperty()
    supporter = ndb.KeyProperty(kind=Supporter)
    content = ndb.KeyProperty(kind=Content)
    compromised = ndb.BooleanProperty()
    code = ndb.StringProperty(default="1234")

    content_id = ndb.IntegerProperty()
    supporter_id = ndb.IntegerProperty()
