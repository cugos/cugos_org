from django.contrib.gis.db import models
from tagging.fields import TagField

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


class Flaws(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    popularity = models.IntegerField(blank=True,null=True)
    severity = models.IntegerField(default=0 )
    geometry = models.PointField(srid=4326)
    tags = TagField()
    objects = models.GeoManager() # so we can use spatial queryset methods
    
    def __unicode__(self): return self.name

    class Meta:
        verbose_name_plural = "Flaws" # otherwise django tries to make the Model name plural

    def get_absolute_url(self):
        self.geometry.transform(900913)
        l = [str(x) for x in self.geometry.extent]
        url = '/map/?extent=%s' % ','.join(l)
        return url
