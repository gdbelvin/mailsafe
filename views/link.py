from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.log import getLogger

from models import Link

logger = getLogger('django.request')

def create(request):
    """
    Create an link.
    """
    content_id = int(request.POST["contentid"])
    supporter_id = int(request.POST["supporterid"])

    link = Link(content_id=content_id, supporter_id=supporter_id, compromised=false)
    link.save()

    return HttpResponse("Created an link: " + " " + name)