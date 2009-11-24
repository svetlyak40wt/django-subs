from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^subscribe/$', 'django_subs.views.subscribe', {}, 'subscribe'),
     (r'^unsubscribe/$', 'django_subs.views.unsubscribe', {}, 'unsubscribe'),
)
