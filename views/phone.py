from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger
from twilio.rest import TwilioRestClient 

logger = getLogger('django.request')

def sms(request, text):
    """
    Test page for sending text messages.
    """
    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN) 
    sms = client.messages.create(
            to="4105416123", 
            from_="+14158892387", 
            body=text,  
    )

    return HttpResponse(sms.sid)

def call(request, text):
    """
    Test page for getting the key pad the user pressed.
    """
    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN) 

    call = client.calls.create(
            to="4105416123", 
            from_="+14158892387", 
            url="mail-safe.appspot.com/twiml/%s" % text,   #URL to find Twitxml
            method="GET",  
            fallback_method="GET",  
            status_callback_method="GET",    
            record="false"
    ) 
     
    return HttpResponse(sms.sid)

def twiml(request, text):
    """
    Handler for generating TwiML
    """
    twiml = """
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather timeout="10" numDigits=1 action="mail-safe.appspot.com/resp/">
        <Say>Hello, are you %s? Press 1 if you are. Press 2 otherwise.</Say>
    </Gather>
</Response>
"""
    return HttpResponse(format(twiml, text))

def resp(request, text):
    print text
    return HttpResponse(text)

