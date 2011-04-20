from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _ # internationalization translate call
from django.contrib.gis.db import models
from django.utils.safestring import mark_safe
from django.conf import settings
import random
import datetime


class UserProfile(models.Model):  
    user = models.ForeignKey(User,verbose_name=_('Username'))
    address = models.CharField(_('Address'),null=True,blank=True,max_length=100)
    uid = models.IntegerField(_('Random User ID'),null=True,blank=True,)

    def __unicode__(self):
        name = self.user.get_full_name()
        if name:
            return unicode("%s" % self.user.get_full_name())
        else:
            return unicode("%s" % self.user.username)          

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def first_name(self):
        return u"%s" % self.user.first_name
    
    def last_name(self):
        return u"%s" % self.user.last_name

    def full_name(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)

    def email(self):
        return u"%s" % self.user.email
        
    def remove(self):
            return '<input type="button" value="Remove" onclick="location.href=\'%s/delete/\'" />' % (self.pk)
    
    remove.short_description = ''
    remove.allow_tags = True
                
    def get_random_id(self):
        rid = random.randint(100000,999999)
        #check to see if random already being used- and call again if not
        return rid
        
    def account_activated(self):
        return self.user.is_active
    account_activated.boolean = True

    def account_diff(self):
        if self.user.is_active:
            return (self.user.date_joined - datetime.datetime.now())

    def save(self, force_insert=False, force_update=False, save_allowed=True):
        if not self.id:
            self.uid = self.get_random_id()
        
        super(UserProfile, self).save()
