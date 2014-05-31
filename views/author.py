from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author
from pprint import pformat

logger = getLogger('django.request')

def create(request):
    """
    Create an author.
    """
    name = request.POST["name"]
    author_email = request.POST["author_email"]

    author = Author(name=name, email=author_email)
    author_id = author.put()

    return HttpResponse("Created an author: %s" % (pformat(author)))

def get(request, email):
    author = Author.query(Author.email == email).get()
    if (author is None):
        return HttpResponseServerError()
    else:
        return HttpResponse(author)

def dump(request):
    """
    Dumps a list of all the authors
    """
    authors = Author.query().fetch()
    return HttpResponse(pformat(authors).replace('\n', '<br/>'))
