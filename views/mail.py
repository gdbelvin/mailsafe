from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from django.core import mail
from google.appengine.ext import ndb
from models import Link, Author, Content

logger = getLogger('django.request')

def send(request):
    """
    Send mail to all contacts of author. Include a link to document x.
    """
    author_id = int(request.POST.get('name', default='0'))
    content_id = int(request.POST.get('content', default='0'))

    # Get the Author and content.
    #author = Author.query(name = author_name).fetch()
    author_key = ndb.Key(Author, author_id)
    author = author_key.get()
    if (author is None): 
        return HttpResponseServerError("Author %s not found" % author_id)
    content_key = ndb.Key(Content, content_id)
    content = content_key.get()
    if (content is None): 
        return HttpResponseServerError("Document %s not found" % content_id)

    # Get a list of all supporters for an author, possibly by group?
    supporters = Supporter.query(of = author.key).fetch()

    # Generate a list of links.
    links = []
    for supporter in supporters:
        link = Link(uuid=uuid.uuid4(), supporter=supporter.key, content=content.key, 
                compromised=False)
        link.put()  # This could be better done in batch mode
        links.append({email:supporter.email, uuid:link.uuid})

    # Send email.
    subject = "Test email"
    message = "Test message"
    from_email = "gdbelvin@wisebold.com"
    # Each element of datatuple is of the format: 
    # (subject, message, from_email, recipient_list)
    datatuple = tuple([(subject, message, from_email, [link['email']]) for link in links])
    mail.send_mass_mail(datatuple, fail_silently=False)

    return HttpResponse("""sent %d emails. <br>
    for %s
    to %s""" % (len(datatuple), author.name, content.key))

def test(request, text):
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
