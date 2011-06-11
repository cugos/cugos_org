from django.contrib.gis.db import models
from cugos_org.tagging.fields import TagField

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()
    geometry = models.PointField(srid=4326)
    objects = models.GeoManager() # so we can use spatial queryset methods
    
    def __unicode__(self): return self.name


class Event(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    url = models.URLField()
    geometry = models.PointField(srid=4326)
    objects = models.GeoManager() # so we can use spatial queryset methods
    
    def __unicode__(self): return self.name
