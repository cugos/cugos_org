from django.contrib.gis.db.models.fields import GeometryField
from django.utils import simplejson
from django.http import HttpResponse

def render_to_geojson(query_set, geom_field=None, mimetype='text/plain', pretty_print=False):
    '''
    
    Shortcut to render a GeoJson FeatureCollection from a Django QuerySet.
    Currently computes a bbox and adds a crs member as a sr.org link
    
    '''
    collection = {}

    # Find the geometry field
    # qs.query._geo_field()

    fields = query_set.model._meta.fields
    geo_fields = [f for f in fields if isinstance(f, GeometryField)]
    
    if len(geo_fields) > 1:
        geo_field = geo_fields[0] # no support yet for multiple geometry fields
    else:
        geo_field = geo_fields[0]
    
    # Gather the projection information
    crs = {}
    crs['type'] = "link"
    crs_properties = {}
    crs_properties['href'] = 'http://spatialreference.org/ref/epsg/%s/' % geo_field._srid
    crs_properties['type'] = 'proj4'
    crs['properties'] = crs_properties 
    collection['crs'] = crs
    
    # Build list of features
    features = []
    if query_set:
      for item in query_set:
         feat = {}
         feat['type'] = 'Feature'
         d= item.__dict__.copy()
         g = getattr(item,geo_field.name)
         d.pop(geo_field.name)
         feat['geometry'] = simplejson.loads(g.geojson)
         feat['properties'] = d
         features.append(feat)
    else:
        pass #features.append({'type':'Feature','geometry': {},'properties':{}})

    # Label as FeatureCollection and add Features
    collection['type'] = "FeatureCollection"    
    collection['features'] = features
    
    # Attach extent of all features
    if query_set:
        collection['bbox'] = [x for x in query_set.extent()]
    
    # Return response
    response = HttpResponse()
    if pretty_print:
        response.write('%s' % simplejson.dumps(collection, indent=1))
    else:
        response.write('%s' % simplejson.dumps(collection))    
    response['Content-length'] = str(len(response.content))
    response['Content-Type'] = mimetype
    return response
