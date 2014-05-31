from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author, Content, Link, Supporter, AuthCode
from twilio.rest import TwilioRestClient 
from random import SystemRandom
import datetime
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

def linkdump(result):
    links = Link.query().fetch()
    return HttpResponse(pformat(links).replace('\n', '<br/>'))

def meta(request, link_id):
    link = Link.query(Link.uuid == link_id).get()
    if (link is None):
        return HttpResponseServerError("bad link")
    supporter = link.supporter.get()
    if (supporter is None):
        return HttpResponseServerError("bad link")
    supporter_name = supporter.name
    return HttpResponse(supporter.name)

def auth(request, link_id):
    link = Link.query(Link.uuid == link_id).get()
    if (link is None):
        return HttpResponseServerError("bad link")
    # Generate new code and timestamp.
    code_len = 5
    code = str(SystemRandom().randint(0, 10**code_len)).zfill(code_len)
    timeout = datetime.datetime.now() + datetime.timedelta(minutes = 5)
    # Try to update
    auth_code = AuthCode.query(AuthCode.uuid == link.key).get()
    if (auth_code is None):
        auth_code = AuthCode(uuid=link.key)
    auth_code.code = code
    auth_code.timeout=timeout
    auth_code.put()

    # Call the phone. 
    supporter = link.supporter.get()
    if (supporter is None):
        return HttpResponseServerError("bad link")

    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN) 
    sms = client.messages.create(
            to=supporter.phone,
            from_="+14158892387", 
            body=code,  
    )
    return HttpResponse("") #Auth Sent
    
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
    return HttpResponse(content.text)
