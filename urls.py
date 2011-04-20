from django.conf.urls.defaults import *
from cugos_main.views import *
from django.conf import settings
from django.contrib import admin

from voting.views import vote_on_object
from cugos_main.models import Flaws
from cugos_main.views import LatestFlaws

admin.autodiscover()

voting_dict = {
    'model': Flaws,
    'template_object_name': 'flaw',
    'allow_xmlhttprequest': True,
}
    

urlpatterns = patterns('',
    #(r'^$', splash),
    (r'^$', main_page),
    (r'^about/', about),
    (r'^projects/', projects),
    (r'^usermap/', user_map),
    (r'^admin/(.*)', admin.site.root),
    #(r'^map/', main_map),
    #(r'^flaws/$', all_flaws),
    #(r'^lookup/$', lookup),
    #(r'^flaws/flaws.json$', as_geojson),
    #(r'^flaws/flaws.kml$', as_kml),
    #(r'^flaws/shapes/$', shape),
    #(r'^flaws/severity/(\d+)/$', flaws_by_severity),
    #(r'^flaws/by_tag/([-_A-Za-z0-9]+)/$', flaws_by_tag),
    #(r'^post_flaw/$', post_flaw),
    #(r'^flaws/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, voting_dict),
    #(r'^flaws/rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict':{'latest':LatestFlaws} }),
    (r'^modelviz/', include('modelviz.urls')),    
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),
    )
    
urlpatterns += patterns('',
        (r'^media/(.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^admin_media/(.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True})

    )
