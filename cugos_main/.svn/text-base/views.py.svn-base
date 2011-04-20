# Django helpers for forming html pages
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from tagging.models import Tag, TaggedItem
from django.contrib.gis.feeds import Feed

# Django authentication 'decorator' - not needed now, but eventually we'll need to 
# register users before posting a flaw
from django.contrib.auth.decorators import login_required

# Geodjango (contrib.gis) helpers
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point

# Models and forms for our app
from cugos_main.models import *
from cugos_main.forms import *
from cugos_main.shortcuts import render_to_geojson

from shapes.views import ShpResponder
import urllib

# geocoding module
#from geopy import geocoders
#g = geocoders.Google(settings.GMAP_API_KEY,output_format='json') 

#def lookup(request):
#		if request.method == 'POST':
#			place, (lat, lon) = g.geocode(request.POST['address'])
#			import pdb;pdb.set_trace()
#			response = HttpResponse()
#			json_response = '{"place":%s,"zoom":%s,"lon":%s,"lat":%s}' % (place,zoom,lon,lat)
#			print json_response
#			response.write(json_response)
#			response['Content-Type'] = "text/plain"
#			return response


def shape(request):
    qs = Flaws.objects.all()
    shp_response = ShpResponder(qs)
    shp_response.readme = 'This is a string of a readme\nplease read this.'
    shp_response.file_name = 'Roadflaw Data'
    #shp_response.geo_field = 'geometry'
    return shp_response()

def lookup(request):
    output_format='json'
    response = HttpResponse()
    if request.method == 'POST':
        location = request.POST.get('address') + ',washington state'
        location = urllib.quote_plus(location)
        geocode = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output_format, settings.GMAP_API_KEY)
        data = urllib.urlopen(geocode).read()
        json = eval(data)
        if json.get('Status').get('code') == 200:
            bbox = json['Placemark'][0]['ExtendedData']['LatLonBox']
            n,s,e,w = bbox['north'],bbox['south'],bbox['east'],bbox['west']
            sw,ne = Point(w,s),Point(e,n)
            e = sw.union(ne).envelope.extent
            bounds = {'a':e[0],'b':e[1],'c':e[2],'d':e[3]}
            response.write(bounds)
            response['Content-Type'] = "text/json"
    else:
        response.write('')
        response['Content-Type'] = "text/json"
    
    return response 

# sample json returned from google
#{'Status': {'code': 200, 'request': 'geocode'}, 'Placemark': [{'Point': {'coordinates': [-122.7982346, 48.562863100000001, 0]}, 'ExtendedData': {'LatLonBox': {'west': -122.830763, 'east': -122.770319, 'north': 48.588596000000003, 'south': 48.531359999999999}}, 'AddressDetails': {'Country': {'CountryName': 'USA', 'AddressLine': ['Blakely Island'], 'CountryNameCode': 'US'}, 'Accuracy': 1}, 'id': 'p1', 'address': 'Blakely Island, United States'}, {'Point': {'coordinates': [-88.023492500000003, 30.723701999999999, 0]}, 'ExtendedData': {'LatLonBox': {'west': -88.040633, 'east': -88.006352000000007, 'north': 30.770814999999999, 'south': 30.676589}}, 'AddressDetails': {'Country': {'CountryName': 'USA', 'AddressLine': ['Blakely Island'], 'CountryNameCode': 'US'}, 'Accuracy': 1}, 'id': 'p2', 'address': 'Blakely Island, United States'}], 'name': 'blakely island'}

def splash(request):
    return render_to_response('splash.html', {})


class LatestFlaws(Feed):
    title = "Roadflaw.com Flaw Feed"
    link = "/sites/rss/latest/"
    description = "Latest Flaws via Roadflaw.com"

    def items(self):
        return Flaws.objects.order_by('-id')[:10]

def main_page(request):
    # Fetch the first 3 events... need to add the order by date
    e = Event.objects.count()
    events = Event.objects.all()[:3]
    f = Flaws.objects.count()
    if f > 3:
      flaws = Flaws.objects.all()
      dissolved = flaws.unionagg()
      dissolved.transform(900913)
      extent = dissolved.extent
    else:
      extent = '(-13644621.04,6028561.02, -13598758.82,6057607.09)'
    if request.method == 'GET' and request.GET.get('extent'):
      extent_string = request.GET.get('extent')
      extent = tuple(map(float,extent_string.split(',')))
    template_vars = {'extent' : extent, 'GMAP_API_KEY': settings.GMAP_API_KEY,'enable_maps':settings.ENABLE_GMAPS, 'events' : events}
    context = RequestContext(request,template_vars)
    return render_to_response('cugos_main/main.html',context)

def user_map(request):
    f = Flaws.objects.count()
    if f > 3:
      flaws = Flaws.objects.all()
      dissolved = flaws.unionagg()
      dissolved.transform(900913)
      extent = dissolved.extent
    else:
      extent = '(-13644621.04,6028561.02, -13598758.82,6057607.09)'
    if request.method == 'GET' and request.GET.get('extent'):
      extent_string = request.GET.get('extent')
      extent = tuple(map(float,extent_string.split(',')))
    template_vars = {'extent' : extent, 'GMAP_API_KEY': settings.GMAP_API_KEY,'enable_maps':settings.ENABLE_GMAPS}
    context = RequestContext(request,template_vars)
    return render_to_response('cugos_usermap/main.html',context)

def projects(request):
    p = Project.objects.count()
    projects = Project.objects.all()
    context = RequestContext(request)
    context['projects'] = projects
    return render_to_response('cugos_projects/main.html',context)

def events(request):
    e = Event.objects.count()
    events = Event.objects.all()
    context = RequestContext(request)
    context['events'] = events
    return render_to_response('cugos_projects/main.html',context)

def about(request):
    f = Flaws.objects.count()
    if f > 3:
      flaws = Flaws.objects.all()
      dissolved = flaws.unionagg()
      dissolved.transform(900913)
      extent = dissolved.extent
    else:
      extent = '(-13644621.04,6028561.02, -13598758.82,6057607.09)'
    if request.method == 'GET' and request.GET.get('extent'):
      extent_string = request.GET.get('extent')
      extent = tuple(map(float,extent_string.split(',')))
    template_vars = {'extent' : extent, 'GMAP_API_KEY': settings.GMAP_API_KEY,'enable_maps':settings.ENABLE_GMAPS}
    context = RequestContext(request,template_vars)
    return render_to_response('cugos_about/main.html',context)

@login_required
def post_flaw(request):
    f = Flaws.objects.count()
    if f > 3:
      flaws = Flaws.objects.all()
      dissolved = flaws.unionagg()
      dissolved.transform(900913)
      extent = dissolved.extent
    else:
      extent = '(-13644621.04,6028561.02, -13598758.82,6057607.09)'
    if request.method == 'POST':
        form = AddFlaw(request.POST)
        if form.is_valid():
          form.save()
          return HttpResponseRedirect('/map/') 
    else:
        if request.method == 'GET' and request.GET.get('extent'):
          extent_string = request.GET.get('extent')
          extent = tuple(map(float,extent_string.split(',')))
        form = AddFlaw()
    template_vars = {'form': form,'extent' : extent, 'GMAP_API_KEY': settings.GMAP_API_KEY,'enable_maps':settings.ENABLE_GMAPS}
    context = RequestContext(request,template_vars)
    return render_to_response('flaws/post_flaw.html',context)
 
def as_kml(request):
    flaws  = Flaws.objects.kml()
    return render_to_kml("kml/placemarks.kml", {'places' : flaws})

def all_flaws(request):
    set = Flaws.objects.all()
    return render_to_geojson(set,mimetype='text/plain')

def flaws_by_tag(request,tag_id):
    query_tag = Tag.objects.get(id=tag_id)
    entries = TaggedItem.objects.get_by_model(Flaws, query_tag.name)
    #entries = entries.order_by('-date')
    return render_to_geojson(entries,mimetype='text/plain')

def flaws_by_severity(request,severity):
    set = Flaws.objects.filter(severity__gte=int(severity))
    return render_to_geojson(set,mimetype='text/plain')

# Same as all_flaws() but will prompt browser to download the geojson features
def as_geojson(request):
    set = Flaws.objects.all()
    return render_to_geojson(set,mimetype='application/json')
