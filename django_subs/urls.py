from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^/$', 'django_subs.views.empty_view'),
)
