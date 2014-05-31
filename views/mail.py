from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger
from django.core import mail

logger = getLogger('django.request')

def send(request, text):
    """
    Test page for sending email messages.
    """
    mails_sent = mail.send_mail('Subject here', 
            'Here is the message.', 
            'gdbelvin@wisebold.com',
            ['gdbelvin@gmail.com'], fail_silently=False)

    return HttpResponse("sent mail: %d" % mails_sent)

def sendall(request, text):
    """
    Test page for sending email messages.
    """
    mail.send_mail(sender_address, user_address, subject, body)

    return HttpResponse(sms.sid)
