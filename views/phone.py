from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger
from models import Author, Content, Link, Supporter, AuthCode
from random import SystemRandom
from twilio.rest import TwilioRestClient 
import twilio.twiml

logger = getLogger('django.request')

def send_sms(link, supporter, code):
    code = generate_code(link)
    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN) 
    sms = client.messages.create(
            to=supporter.phone,
            from_="+14158892387", 
            body=code,  
    )

def gen_twiml(request, uuid):
    code = generate_code(link)
    link = Link.query(Link.uuid == uuid).get()
    if (link is None):
        return HttpResponseNotFound("bad link")
    supporter = link.supporter.get()
    if (supporter is None):
        return HttpResponseNotFound("bad link")

    resp = twilio.twiml.Response()
    resp.say("Hello, %s. Here is your code, %s" % (supporter.name, code))
    return HttpResponse(str(resp))

def call_phone(link, supporter):
    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN) 
    call = client.calls.create(
            to=supporter.phone, 
            from_="+14158892387", 
            url="%s/twiml/%s" %(settings.SERVER, link.uuid),
            method="GET",  
            fallback_method="GET",  
            status_callback_method="GET",    
            record="false"
    ) 

def auth(request, uuid):
    link = Link.query(Link.uuid == uuid).get()
    if (link is None):
        return HttpResponseServerError("bad link")
    supporter = link.supporter.get()
    if (supporter is None):
        return HttpResponseServerError("bad link")
    if False:
        send_sms(link, supporter)
    else:
        call_phone(link, supporter)

    return HttpResponse("Auth Sent") #Auth Sent
