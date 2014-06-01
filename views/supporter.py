from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError, HttpResponseNotFound
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Supporter, Author
import json_fixed

logger = getLogger('django.request')

def create(request):
    """
    Create an supporter.
    """
    name = request.POST["name"]
    phone = request.POST["phone"]
    email = request.POST["email"]
    author_email = request.POST["author_email"]

    author = Author.query(Author.email == email).get()
    if (author is None): 
        return HttpResponseServerError("Author %s not found" % author_email)
    
    supporter = Author.query(Author.email == email).get()
    if(supporter is None):
        supporter = Supporter(name=name, email=email, phone=phone, of=[author.key])
    else:
        supporter.name = name
        supporter.email = email
        supporter.phone = phone
        
    supporter.put()
    return HttpResponse(json_fixed.dumps(supporter))

def get(request, email):
    supporter = Author.query(Author.email == email).get()
    if (supporter is None):
        return HttpResponseNotFound()
    return HttpResponse(json_fixed.dumps(supporter))

def dump(request):
    """
    Dumps a list of all the supporters.
    """
    supporters = Supporter.query().fetch()
    return HttpResponse(json_fixed.dumps(supporters))
