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
    # Author
    (r'^author/create$', 'views.author.create'),
    (r'^author/dump$', 'views.author.dump'),
    (r'^author/(.*)/supporters$', 'views.author.get_supporters'), 
    (r'^author/(.*)/documents$', 'views.author.get_documents'), 
    (r'^author/(.*)$', 'views.author.get'),
    # Supporter
    (r'^supporter/create$', 'views.supporter.create'),
    (r'^supporter/dump$', 'views.supporter.dump'),
    (r'^supporter/(.*)$', 'views.supporter.rest'), # POST, DELETE, GET
    # Doc
    (r'^doc/create$', 'views.doc.create'),
    (r'^doc/dump$', 'views.doc.dump'), #DEBUG
    (r'^doc/(.*)/send$', 'views.doc.send'),
    (r'^doc/(.*)$', 'views.doc.rest'), # POST, DELETE, GET
    # Letter - obfuscated links
    (r'^letter/dump$', 'views.letter.linkdump'), #DEBUG
    (r'^letter/(.*)/auth$', 'views.phone.auth'),
    (r'^letter/(.*)/(.*)$', 'views.letter.get'), # doc/id/auth_code
    (r'^letter/(.*)$', 'views.letter.meta'), # doc/id
)
