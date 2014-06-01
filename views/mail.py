from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone, HttpResponseServerError
from django.utils.log import getLogger
from django.core import mail
from google.appengine.ext import ndb
from models import Link, Author, Content, Supporter
import uuid

logger = getLogger('django.request')

def send(request):
    """
    Send mail to all contacts of author. Include a link to document x.
    """
    author_email = request.POST['author_email']
    content_id = int(request.POST.get('content_id', default='0'))

    # Get the Author and content.
    #author = Author.query(name = author_name).fetch()
    author = Author.query(Author.email == author_email).get()
    if (author is None): 
        return HttpResponseServerError("Author %s not found" % author_email)
    content_key = ndb.Key(Content, content_id)
    content = content_key.get()
    if (content is None): 
        return HttpResponseServerError("Document %s not found" % content_id)

    # Get a list of all supporters for an author, possibly by group?
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
The MailSafe Team"""
    from_email = "gdbelvin@wisebold.com"

    # Each element of datatuple is of the format: 
    # (subject, message, from_email, recipient_list)
    datatuple = tuple([(subject, message % (link['supporter_name'], author.name, link['uuid']), from_email, [link['email']]) for link in links])
    mail.send_mass_mail(datatuple, fail_silently=False)

    return HttpResponse("sent %d emails on behalf of %s for doc %s to %s" % (len(datatuple), author.name, content.key, datatuple))