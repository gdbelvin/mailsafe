# App Engine Datastore model, "webapp/main.py"
from google.appengine.ext import db

class Supporter(db.Model):
    name = db.TextProperty()
    email = db.TextProperty()
    phone = db.TextProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)