from django.conf.urls.defaults import *
from django.contrib import admin
import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
    ('^d/.*$', 'django.views.generic.simple.direct_to_template', {'template': 'viewdoc.html'}),
    ('^v/.*$', 'django.views.generic.simple.direct_to_template', {'template': 'verifyid.html'}),
    ('^admin/', include(admin.site.urls)),

    # Twilio callbacks
    (r'^twiml/(.*)$', 'views.phone.gen_twiml'),
    # Mail
    (r'^mail/send$', 'views.mail.send'),
    # Author
    (r'^author/create$', 'views.author.create'),
    (r'^author/dump$', 'views.author.dump'),
    (r'^author/(.*)/supporters$', 'views.author.get_supporters'), 
    (r'^author/(.*)/documents$', 'views.author.get_documents'), 
    (r'^author/(.*)$', 'views.author.get'),
    # Supporter
    (r'^supporter/create$', 'views.supporter.create'),
    (r'^supporter/dump$', 'views.supporter.dump'),
    (r'^supporter/(.*)$', 'views.supporter.get'),
    # Doc
    (r'^doc/create$', 'views.doc.create'),
    (r'^doc/dump$', 'views.doc.dump'), #DEBUG
    # Link
    (r'^doc/(.*)/auth$', 'views.phone.auth'),
    (r'^doc/(.*)/(.*)$', 'views.doc.get'), # doc/id/auth_code
    (r'^doc/(.*)$', 'views.doc.meta'), # doc/id
    (r'^link/dump$', 'views.doc.linkdump'), #DEBUG
)
