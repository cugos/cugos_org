from django.contrib.gis import admin
from cugos_org.batchadmin.admin import BatchModelAdmin
from cugos_org.profiles.models import *

class BA(BatchModelAdmin):
  actions_on_top = False

class UserProfileAdmin(BA):
    pass#list_display = ('user', 'full_name','email','account_activated','account_diff','remove',)
    #list_filter = (' ',)

admin.site.register(UserProfile, UserProfileAdmin)
