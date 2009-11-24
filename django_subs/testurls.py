from django.conf.urls.defaults import *
from django.http import HttpResponse

def empty_view(request):
    return HttpResponse('')

urlpatterns = patterns('',
     (r'^$', empty_view),
     (r'^subs/', include('django_subs.urls')),
)

