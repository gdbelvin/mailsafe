from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from models import Author, Content, Link, Supporter, AuthCode
from random import SystemRandom
from twilio.rest import TwilioRestClient 
import twilio.twiml

logger = getLogger('django.request')

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
    method = request.POST["method"]
    link = Link.query(Link.uuid == uuid).get()
    if (link is None):
        return HttpResponseServerError("bad link")
    supporter = link.supporter.get()
    if (supporter is None):
        return HttpResponseServerError("bad link")
    if (method == "sms"):
        send_sms(link, supporter)
    else:
        call_phone(link, supporter)

    return HttpResponse("Auth Sent")
