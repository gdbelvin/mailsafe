from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError, HttpResponseNotFound
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

def create(request):
    author_email = request.POST["author_email"]
    text = request.POST["text"]
    subject = request.POST.get("subject")
    status = request.POST.get('status')

    author = Author.query(Author.email == author_email).get()
    if (author is None):
        return HttpResponseServerError("Author %s not found" % author_id)

    content = Content(author=author.key, text=text, subject=subject,
            status="draft")
    content.put()

    resp = content.to_dict()
    resp['content_id'] = content.key.id()

    return HttpResponse(json_fixed.dumps(resp))

def update(request, content_id):
    author_email = request.POST["author_email"]
    text = request.POST["text"]
    subject = request.POST.get("subject")
    status = request.POST.get('status')

    content = ndb.Key(Content, int(content_id)).get()
    if (content is None):
        return HttpResponseNotFound("No doc found.")

    content.text = text
    if (subject is not None):
        content.subject = subject
    if (status is not None):
        context.status = status
    context.date_updated = datetime.datetime.now()
    content.put()
    return HttpResponse(json_fixed.dumps(content))

def delete(request, content_id):
    content = ndb.Key(Content, int(content_id)).get()
    if (content is None):
        return HttpResponseNotFound("No doc found.")
    content.delete()
    return HttpResponse()

def dump(result):
    docs = Content.query().fetch()
    return HttpResponse(json_fixed.dumps(docs))

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

def get(request, link_id, sms_code):
    dlink = Link.query(Link.uuid == link_id).get()
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
