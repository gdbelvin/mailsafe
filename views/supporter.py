from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError, HttpResponseNotFound
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Supporter, Author
import json_fixed

logger = getLogger('django.request')

def create(request):
    name = request.POST["name"]
    phone = request.POST["phone"]
    email = request.POST["email"]
    author_email = request.POST["author_email"]

    author = Author.query(Author.email == author_email).get()
    if (author is None): 
        return HttpResponseServerError("Author %s not found" % author_email)
    
    supporter = Supporter(name=name, email=email, phone=phone, of=[author.key])
    supporter.put()
    return HttpResponse(json_fixed.dumps(supporter))

def update(request, author_email):
    name = request.POST["name"]
    phone = request.POST["phone"]
    email = request.POST["email"]

    supporter = Supporter.query(Supporter.email == email).get()
    if (supporter is None):
        return HttpResponseNotFound()

    supporter.name = name
    supporter.email = email
    supporter.phone = phone
    supporter.put()
    return HttpResponse(json_fixed.dumps(supporter))

def get(request, email):
    supporter = Supporter.query(Supporter.email == email).get()
    if (supporter is None):
        return HttpResponseNotFound()
    return HttpResponse(json_fixed.dumps(supporter))

def delete(request, email):
    supporter = Supporter.query(Supporter.email == email).get()
    if (supporter is None):
        return HttpResponseNotFound()
    supporter.key.delete()
    return HttpResponse(json_fixed.dumps(supporter))

def dump(request):
    supporters = Supporter.query().fetch()
    return HttpResponse(json_fixed.dumps(supporters))

def rest(request, email):
    if request.method == 'POST':
        return update(request, email)
    elif request.method == 'GET':
        return get(request, email)
    elif request.method == 'DELETE':
        return delete(request, email)
