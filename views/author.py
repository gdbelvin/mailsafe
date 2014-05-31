from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger

from google.appengine.ext import ndb

from models import Author

logger = getLogger('django.request')

def create(request):
    """
    Create an author.
    """
    name = request.POST["name"]

    author = Author(name=name)
    author_id = author.put().id()

    return HttpResponse("Created an author: %s %s " % (name, author_id))

def get(request, text):
    author = ndb.Key(Author, int(text)).get()
    return HttpResponse(author)