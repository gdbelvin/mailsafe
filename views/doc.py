from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from google.appengine.ext import ndb
from models import Author, Content, Link, Supporter, AuthCode
from twilio.rest import TwilioRestClient 
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

    if (request.POST.__contains__("content_id")):
        content_id = request.POST["content_id"]
        content = ndb.Key(Content, int(content_id)).get()
        content.subject = subject
        content.text = text
        content.put()
        return HttpResponse(json_fixed.dumps(content))
    else:
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

def auth(request, link_id):
    link = Link.query(Link.uuid == link_id).get()
    if (link is None):
        return HttpResponseServerError("bad link")
    # Generate new code and timestamp.
    code_duration = 5
    code = str(SystemRandom().randint(0, 10**code_duration)).zfill(code_duration)
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
    return HttpResponse("Auth Sent") #Auth Sent
    
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
