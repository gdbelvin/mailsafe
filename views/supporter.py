from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Supporter, Author
from pprint import pformat
import json

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

<<<<<<< HEAD
def get(request, email):
    supporter = Author.query(Author.email == email).get()
    return HttpResponse(supporter)
=======
def get(request, text):
    supporter = ndb.Key(Supporter, int(text)).get()
    del supporters[x].date_created
    return HttpResponse(json.dumps(supporters[x].to_dict()))
>>>>>>> d7fcb61adbc05620854949dc838269eb39aa6511

def dump(request):
    """
    Dumps a list of all the supporters.
    """
    output = "["
    supporters = Supporter.query().fetch()
    for x in range(0,len(supporters)):
       del supporters[x].date_created
       output +=json.dumps(supporters[x].to_dict())
       if x==(len(supporters)-1):
         output +="]"
       else:
         output+=", "
    return HttpResponse(output)
