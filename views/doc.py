from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author, Content, Link, Supporter
from pprint import pformat

logger = getLogger('django.request')

def create(request):
    """
    Create a document.
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

def get(request, link_id, sms_code):
    link = ndb.Key(Link, int(link_id)).get()
    doc_id = int(link.content_id)
    doc = ndb.Key(Content, doc_id).get()
    db_sms_code = link.code
    if(sms_code != db_sms_code):
        return HttpResponse("", None, 403) #Unauthorized
    return HttpResponse("%s %s" % (doc_id, doc))
    
def meta(request, link_id):
    link = ndb.Key(Link, int(link_id)).get()
    supporter_id = int(link.supporter_id)
    supporter = ndb.Key(Supporter, supporter_id).get()
    supporter_name = supporter.name
    return HttpResponse(supporter.name)