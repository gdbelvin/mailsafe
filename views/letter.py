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
import uuid

def linkdump(result):
    links = Link.query().fetch()
    return HttpResponse(json_fixed.dumps(links))

def meta(request, link_id):
    link = Link.query(Link.uuid == link_id).get()
    if (link is None):
        return HttpResponseNotFound("bad link")
    supporter = link.supporter.get()
    if (supporter is None):
        return HttpResponseNotFound("bad link")
    ret = {'name': supporter.name}
    return HttpResponse(json.dumps(ret), status=401)

def get(request, link_id, sms_code):
    link = Link.query(Link.uuid == link_id).get()
    if (link is None):
        return HttpResponseServerError("bad link")

    authcode = AuthCode.query(AuthCode.uuid == link.key).get()
    if (authcode is None):
        return HttpResponseServerError("bad link")
            
    content = link.content.get()
    if(content.status != "published"):
        return HttpResponseServerError("deactivated link")

    # Verify code
    if (sms_code != authcode.code):
        return HttpResponse("bad code", None, 403) #Unauthorized

    # check timestamp
    now = datetime.datetime.now()
    if (now > authcode.timeout):
        return HttpResponse("timeout", None, 403) #Unauthorized

    if (content is None):
        return HttpResponseServerError("bad link")
    return HttpResponse(json_fixed.dumps(content))
