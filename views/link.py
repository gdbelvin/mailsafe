from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger
from pprint import pformat

from google.appengine.ext import ndb

from models import Link

logger = getLogger('django.request')

def create(request):
    """
    Create an link.
    """
    content_id = int(request.POST["contentid"])
    supporter_id = int(request.POST["supporterid"])

    link = Link(content_id=content_id, supporter_id=supporter_id, compromised=False)
    link_id = link.put().id()

    return HttpResponse("Created an link: %s %s %s" % (content_id, supporter_id, link_id))

def dump(result):
    """
    Dumps the contents of all links.
    """
    links = Link.query().fetch()
    return HttpResponse(pformat(links).replace('\n', '<br/>'))

def get(request, text):
    link = ndb.Key(Link, int(text)).get()
    return HttpResponse(link)