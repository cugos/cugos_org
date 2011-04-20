from django.contrib.gis.db import models
from django.utils.translation import ungettext
from django.utils.encoding import force_unicode
from django.contrib.gis import admin
from django.contrib.admin.views.main import ChangeList


def model_format_dict(obj):
    """
    Return a `dict` with keys 'verbose_name' and 'verbose_name_plural',
    typically for use with string formatting.
    
    `obj` may be a `Model` instance, `Model` subclass, or `QuerySet` instance.
    
    """
    if isinstance(obj, (models.Model, models.base.ModelBase)):
        opts = obj._meta
    elif isinstance(obj, models.query.QuerySet):
        opts = obj.model._meta
    else:
        opts = obj
    return {
        'verbose_name': force_unicode(opts.verbose_name),
        'verbose_name_plural': force_unicode(opts.verbose_name_plural)
    }

def model_ngettext(obj, n=None):
    """
    Return the appropriate `verbose_name` or `verbose_name_plural` for `obj`
    depending on the count `n`.
    
    `obj` may be a `Model` instance, `Model` subclass, or `QuerySet` instance.
    If `obj` is a `QuerySet` instance, `n` is optional and the length of the
    `QuerySet` is used.
    
    """
    if isinstance(obj, models.query.QuerySet):
        if n is None:
            n = obj.count()
        obj = obj.model
    d = model_format_dict(obj)
    return ungettext(d['verbose_name'], d['verbose_name_plural'], n or 0)

def get_changelist(request, model, model_admin=None):
    if model_admin is None:
        model_admin = admin.site._registry[model]
    return ChangeList(
        request, model, model_admin.list_display,
        model_admin.list_display_links, model_admin.list_filter,
        model_admin.date_hierarchy, model_admin.search_fields,
        model_admin.list_select_related, model_admin.list_per_page,
        model_admin
    )
