from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author, Content, Link, Supporter, AuthCode
from twilio.rest import TwilioRestClient 
import twilio.twiml
from random import SystemRandom
import datetime
import json_fixed
import json

logger = getLogger('django.request')

# TODO: support uploading files.
def create(request):
    """
    Create a document.
    """
    author_email = request.POST["author_email"]
    text = request.POST["text"]
    subject = request.POST["subject"]

    author = Author.query(Author.email == author_email).get()
    if (author is None):
        return HttpResponseServerError("Author %s not found" % author_id)
    content = Content(author=author.key, text=text, subject=subject)
    content.put()

    resp = content.to_dict()
    resp['content_id'] = content.key.id()
    del resp['author']

    return HttpResponse(json.dumps(resp))

def dump(result):
    """
    Dumps the contents of all documents.
    """
    contents = Content.query().fetch()
    return HttpResponse(json_fixed.dumps(contents))

def linkdump(result):
    links = Link.query().fetch()
    return HttpResponse(json_fixed.dumps(links))

def meta(request, link_id):
    link = Link.query(Link.uuid == link_id).get()
    if (link is None):
        return HttpResponseServerError("bad link")
    supporter = link.supporter.get()
    if (supporter is None):
        return HttpResponseServerError("bad link")
    supporter_name = supporter.name
    return HttpResponse(supporter.name)

def generate_code(link):
    # Generate new code and timestamp.
    # Saves code to AuthCode table
    code_len = 5
    code_duration = 5 # Minutes.
    code = str(SystemRandom().randint(0, 10**code_len)).zfill(code_len)
    timeout = datetime.datetime.now() + datetime.timedelta(minutes = code_duration)
    # Try to update
    auth_code = AuthCode.query(AuthCode.uuid == link.key).get()
    if (auth_code is None):
        auth_code = AuthCode(uuid=link.key)
    auth_code.code = code
    auth_code.timeout=timeout
    auth_code.put()
    return code

def get(request, link_id, sms_code):
    link = Link.query(Link.uuid == link_id).get()
    if (link is None):
        return HttpResponseServerError("bad link")

    authcode = AuthCode.query(AuthCode.uuid == link.key).get()
    if (authcode is None):
        return HttpResponseServerError("bad link")
    
    # Verify code
    if (sms_code != authcode.code):
        return HttpResponse("bad code: %s" % authcode.code, None, 403) #Unauthorized

    # check timestamp
    now = datetime.datetime.now()
    if (now > authcode.timeout):
        return HttpResponse("timeout", None, 403) #Unauthorized

    content = link.content.get()
    if (content is None):
        return HttpResponseServerError("bad link")
    return HttpResponse(json_fixed.dumps(content))
