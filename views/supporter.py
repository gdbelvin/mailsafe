from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger

from google.appengine.ext import ndb

from models import Supporter

logger = getLogger('django.request')

def create(request):
    """
    Create an supporter.
    """
    name = request.POST["name"]
    phone = request.POST["phone"]
    email = request.POST["email"]

    supporter = Supporter(name=name, email=email, phone=phone)
    supporter_id = supporter.put().id()

    return HttpResponse("Created an supporter: %s %s %s %s" % (name, phone, email, supporter_id))

def get(request, text):
    supporter = ndb.Key(Supporter, int(text)).get()
    return HttpResponse(supporter)