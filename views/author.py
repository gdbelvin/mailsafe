from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError, HttpResponseNotFound
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author
from pprint import pformat
import json

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
        return HttpResponseNotFound()
    else:
        return HttpResponse(author)

def dump(request):
    """
    Dumps a list of all the authors
    """

    output = "["
    authors = Author.query().fetch()
    for x in range(0,len(authors)):
       output +=json.dumps(authors[x].to_dict())
       if x==(len(authors)-1):
         output +="]"
       else:
         output+=", "
    return HttpResponse(output)
