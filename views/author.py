from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError, HttpResponseNotFound
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author
import json_fixed

logger = getLogger('django.request')

def create(request):
    """
    Create an author.
    """
    name = request.POST["author_name"]
    author_email = request.POST["author_email"]

    author = Author(name=name, email=author_email)
    author_id = author.put()

    return HttpResponse(json_fixed.dumps(author))

def get(request, email):
    author = Author.query(Author.email == email).get()
    if (author is None):
        return HttpResponseNotFound()
    else:
        return HttpResponse(json_fixed.dumps(author))

def dump(request):
    """
    Dumps a list of all the authors
    """

    authors = Author.query().fetch()
    output = "[" + ", ".join([json_fixed.dumps(x) for x in authors]) + "]"
    return HttpResponse(output)
