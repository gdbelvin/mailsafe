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
    return HttpResponse(json_fixed.dumps(content))

def get(request, content_id):
    content = ndb.Key(Content, int(content_id)).get()
    if (content is None):
        return HttpResponseNotFound("No doc found.")
    return HttpResponse(json_fixed.dumps(content))

def update(request, content_id):
    author_email = request.POST["author_email"]
    text = request.POST["text"]
    subject = request.POST.get("subject")
    status = request.POST.get('status')
    
    content = ndb.Key(Content, int(content_id)).get()
    if (content is None):
        return HttpResponseNotFound("No doc found.")

    if(text is not None):
        content.text = text
    if (subject is not None):
        content.subject = subject
    if (status is not None):
        content.status = status
    content.date_updated = datetime.datetime.now()
    content.put()
    return HttpResponse(json_fixed.dumps(content))

def delete(request, content_id):
    content = ndb.Key(Content, int(content_id)).get()
    if (content is None):
        return HttpResponseNotFound("No doc found.")
    content.key.delete()
    return HttpResponse()

def dump(result):
    docs = Content.query().fetch()
    return HttpResponse(json_fixed.dumps(docs))

def rest(request, content_id):
    if request.method == 'POST':
        return update(request, content_id)
    elif request.method == 'GET':
        return get(request, content_id)
    elif request.method == 'DELETE':
        return delete(request, content_id)

def send(request, content_id):
    """
    Send mail to all contacts of author. Include a link to document x.
    """
    content_key = ndb.Key(Content, int(content_id))
    content = content_key.get()
    if (content is None): 
        return HttpResponseServerError("Document %s not found" % content_id)

    author = content.author.get()
    if (author is None): 
        return HttpResponseServerError("Author %s not found" % author_email)

    supporters = Supporter.query(Supporter.of == author.key).fetch()

    # Generate a list of links.
    links = []
    for supporter in supporters:
        link = Link(uuid=uuid.uuid4().get_hex(), supporter=supporter.key, content=content.key, 
                compromised=False)
        link.put()  # This could be better done in batch mode
        links.append({"email":supporter.email, "uuid":link.uuid, "supporter_name":supporter.name})

    # Send email.
    subject = "A MailSafe Message From %s" % author.name
    message = """Dear %s,\n
You have received a message from %s through MailSafe. Please click on the following link to view their message:\n
https://mail-safe.appspot.com/doc/%s\n
https://mailsafe.herokuapp.com/public/letter/%s\n
The MailSafe Team"""
    from_email = "gdbelvin@wisebold.com"

    # Each element of datatuple is of the format: 
    # (subject, message, from_email, recipient_list)
    datatuple = tuple([(subject, message % (link['supporter_name'], author.name, link['uuid'], link['uuid']), from_email, [link['email']]) for link in links])
    mail.send_mass_mail(datatuple, fail_silently=False)

    return HttpResponse("sent %d emails on behalf of %s for doc %s to %s" % (len(datatuple), author.name, content.key, datatuple))
