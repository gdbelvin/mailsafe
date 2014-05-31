from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger

from mailsafe.models import Author

logger = getLogger('django.request')

def create(request):
    """
    Create an author.
    """
    name = request.POST["name"]

    author = Author(name=name)
    author.save()

    return HttpResponse("Created an author: " + " " + name)