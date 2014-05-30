from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger
from twilio.rest import TwilioRestClient 

logger = getLogger('django.request')

def text(request, text):
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

