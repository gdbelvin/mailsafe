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
    (r'^sms/(.*)$', 'views.phone.sms'),
    (r'^call/(.*)$', 'views.phone.call'),
    (r'^twiml/(.*)$', 'views.phone.twiml'),
    ('^admin/', include(admin.site.urls)),
)
