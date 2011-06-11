from django.contrib import admin
from cugos_org.tagging.models import Tag, TaggedItem

admin.site.register(TaggedItem)
admin.site.register(Tag)
