from django.conf.urls.defaults import *
from cugos_main.views import *
from django.conf import settings
from django.contrib import admin
from django.contrib import databrowse
from voting.views import vote_on_object

admin.autodiscover()

# voting_dict = {
#     'model': Flaws,
#     'template_object_name': 'flaw',
#     'allow_xmlhttprequest': True,
# }
    

urlpatterns = patterns('',
    #(r'^$', splash),
    (r'^$', main_page),
    (r'^about/', about),
    (r'^projects/', projects),
    (r'^usermap/', user_map),
    (r'^admin/', include(admin.site.urls)),
    #(r'^map/', main_map),
    #(r'^modelviz/', include('modelviz.urls')),    
    #(r'^accounts/', include('registration.urls')),
    #(r'^profiles/', include('profiles.urls')),
    #(r'^databrowse/(.*)', databrowse.site.root),
    )
    
urlpatterns += patterns('',
        (r'^media/(.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^admin_media/(.*)$','django.views.static.serve',{'document_root': settings.ADMIN_MEDIA_ROOT, 'show_indexes': True})

    )
