from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Supporter
from pprint import pformat

logger = getLogger('django.request')

def create(request):
    """
    Create an supporter.
    """
    name = request.POST["name"]
    phone = request.POST["phone"]
    email = request.POST["email"]

    supporter = Supporter(name=name, email=email, phone=phone)
    supporter.put()

    return HttpResponse("Created a supporter: %s" % (supporter))

def get(request, text):
    supporter = ndb.Key(Supporter, int(text)).get()
    return HttpResponse(supporter)

def dump(request):
    """
    Dumps a list of all the supporters.
    """
    supporters = Supporter.query().fetch()
    return HttpResponse(pformat(supporters).replace('\n', '<br/>'))
