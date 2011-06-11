from django.contrib.gis import admin
from cugos_org.cugos_main.models import *

class ProjectAdmin(admin.OSMGeoAdmin):
    #list_display = ('name')
    search_fields = ('name','description',)
    
    scrollable = False
    map_width = 550
    map_height = 350
    openlayers_url = '/media/js/openlayers/OpenLayers.js'
    extra_js = ['/media/js/openlayers/OpenStreetMap.js']

class EventAdmin(admin.OSMGeoAdmin):
    #list_display = ('name')
    search_fields = ('name','description',)
    
    scrollable = False
    map_width = 550
    map_height = 350
    openlayers_url = '/media/js/openlayers/OpenLayers.js'
    extra_js = ['/media/js/openlayers/OpenStreetMap.js']

class FlawAdmin(admin.OSMGeoAdmin):
    list_display = ('name','severity','tags')
    list_filter = ('tags','severity',)
    search_fields = ('name','description',)
    
    scrollable = False
    map_width = 750
    map_height = 450
    openlayers_url = '/media/js/openlayers/OpenLayers.js'
    extra_js = ['/media/js/openlayers/OpenStreetMap.js']

# Register our model and admin options with the admin site
#admin.site.register(Flaws, FlawAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Event, EventAdmin)

