from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError, HttpResponseNotFound
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author, Supporter, Content
import json_fixed

logger = getLogger('django.request')

def create(request):
    """
    Create an author.
    """
    name = request.POST["author_name"]
    author_email = request.POST["author_email"]

    author = Author.query(Author.email == author_email).get()
    if (author is None):
        author = Author(name=name, email=author_email)
    else:
        author.name = name
        
    author.put()
    return HttpResponse(json_fixed.dumps(author))

def get(request, author_email):
    author = Author.query(Author.email == author_email).get()
    if (author is None):
        return HttpResponseNotFound()
    return HttpResponse(json_fixed.dumps(author))

def dump(request):
    """
    Dumps a list of all the authors
    """
    authors = Author.query().fetch()
    return HttpResponse(json_fixed.dumps(authors))

def get_supporters(request, author_email):
    author = Author.query(Author.email == author_email).get()
    if (author is None):
        return HttpResponseNotFound()
    supporters = Supporter.query(Supporter.of == author.key).fetch()
    return HttpResponse(json_fixed.dumps(supporters))

def get_documents(request, author_email):
    author = Author.query(Author.email == author_email).get()
    if (author is None):
        return HttpResponseNotFound()
    documents = Content.query(Content.author == author.key).fetch()
    return HttpResponse(json_fixed.dumps(documents))
