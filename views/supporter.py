from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Supporter, Author
from pprint import pformat

logger = getLogger('django.request')

def create(request):
    """
    Create an supporter.
    """
    name = request.POST["name"]
    phone = request.POST["phone"]
    email = request.POST["email"]
    author_email = request.POST["author_email"]

    author = Author.query(Author.email == email).get()
    if (author is None): 
        return HttpResponseServerError("Author %s not found" % author_email)

    supporter = Supporter(name=name, email=email, phone=phone, of=[author.key])
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
