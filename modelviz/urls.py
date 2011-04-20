from django.conf.urls.defaults import *

from modelviz.views import *

urlpatterns = patterns('',
    (r'^$',graph),
    (r'^(.*)/$',graph_app),    
    )