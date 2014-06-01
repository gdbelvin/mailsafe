from django.db import models
from google.appengine.ext import ndb

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
    subject = ndb.StringProperty()
    text = ndb.TextProperty()
    author = ndb.KeyProperty(kind=Author)
    status = ndb.StringProperty()
    date_updated = ndb.DateTimeProperty(auto_now_add=True)
    date_created = ndb.DateTimeProperty(auto_now_add=True)

class Link(ndb.Model):
    uuid = ndb.StringProperty()
    supporter = ndb.KeyProperty(kind=Supporter)
    content = ndb.KeyProperty(kind=Content)
    compromised = ndb.BooleanProperty()

class AuthCode(ndb.Model):
    code = ndb.StringProperty() 
    timeout = ndb.DateTimeProperty()
    uuid = ndb.KeyProperty(kind=Link)
