from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author, Content
from pprint import pformat

logger = getLogger('django.request')

def upload(request):
    """
    upload a document.
    """
    author_id = int(request.POST["author_id"])
    text = request.POST["text"]
    # TODO: support uploading files.

    author_key = ndb.Key(Author, author_id)
    author = author_key.get()
    if (author is None):
        return HttpResponseServerError("Author %s not found" % author_id)
    content = Content(author=author.key, text=text)
    content.put()

    return HttpResponse("Created a document: %s" % (content))

def dump(result):
    """
    Dumps the contents of all documents.
    """
    contents = Content.query().fetch()
    return HttpResponse(pformat(contents).replace('\n', '<br/>'))

def get(request, text):
    # TODO: implement
    return HttpResponse("")


