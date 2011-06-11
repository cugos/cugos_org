from django.contrib.gis import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from cugos_org.batchadmin.forms import ActionForm, checkbox, CHECKBOX_NAME
from cugos_org.batchadmin.util import model_format_dict, model_ngettext, get_changelist


class BatchModelAdmin(admin.OSMGeoAdmin):
    change_list_template = "batchadmin/change_list.html"
    list_display = ['batchadmin_checkbox'] + list(admin.OSMGeoAdmin.list_display)
    batch_actions = ['delete_selected']
    batch_action_form = ActionForm
    actions_on_top = True
    actions_on_bottom = True
    
    def __init__(self, *args, **kwargs):
        """
        After initializing `admin.ModelAdmin`, ensure that `list_display`
        contains 'batchadmin_checkbox' and that `list_display_links` won't try
        to link the checkbox.
        
        """
        super(BatchModelAdmin, self).__init__(*args, **kwargs)
        if 'batchadmin_checkbox' not in self.list_display:
            self.list_display = list(self.list_display)
            self.list_display.insert(0, 'batchadmin_checkbox')
        if not self.list_display_links:
            for name in self.list_display:
                if name != 'batchadmin_checkbox':
                    self.list_display_links = [name]
                    break
    
    def batchadmin_checkbox(self, object):
        """A `list_display` column containing a checkbox widget."""
        return checkbox.render(CHECKBOX_NAME, str(object.pk))
    batchadmin_checkbox.short_description = mark_safe('&#x2713;')
    batchadmin_checkbox.allow_tags = True
    
    def delete_selected(self, request, changelist):
        if self.has_delete_permission(request):
            selected = request.POST.getlist(CHECKBOX_NAME)
            objects = changelist.get_query_set().filter(pk__in=selected)
            n = objects.count()
            if n:
                for obj in objects:
                    object_repr = str(obj)
                    self.log_deletion(request, obj, object_repr)
                objects.delete()
                self.message_user(request, "Successfully deleted %d %s." % (
                    n, model_ngettext(self.opts, n)
                ))
    delete_selected.short_description = "Delete selected %(verbose_name_plural)s"
    
    def _get_batchadmin_choices(self):
        actions = getattr(self, 'batch_actions', [])
        choices = []
        for action in actions:
            func = getattr(self, action)
            description = getattr(func, 'short_description', None)
            if description is None:
                description = capfirst(action.replace('_', ' '))
            choice = (action, description % model_format_dict(self.opts))
            choices.append(choice)
        return choices
    batchadmin_choices = property(_get_batchadmin_choices)
    
    def batchadmin_dispatch(self, request, changelist, action):
        """
        Get the batch action named `action` and call it with `request` and
        `changelist` as arguments. `action` must be a callable attribute on
        the `BatchModelAdmin` instance.
        
        """
        action_func = getattr(self, action, None)
        if callable(action_func):
            return action_func(request, changelist)
    
    def changelist_view(self, request, extra_context=None):
        """
        Render the change list with checkboxes for each object and a menu
        for performing batch actions. Submitting the action form POSTs back
        to this view, where it is dispatched to the appropriate handler.
        
        """
        choices = self.batchadmin_choices
        if request.method == 'POST':
            changelist = get_changelist(request, self.model, self)
            
            # There can be multiple action forms on the page (at the top
            # and bottom of the change list, for example). Get the action
            # whose button was pushed.
            action_index = int(request.POST.get('index', 0))
            data = {}
            for key in request.POST:
                if key not in (CHECKBOX_NAME, 'index'):
                    data[key] = request.POST.getlist(key)[action_index]
            action_form = self.batch_action_form(data, auto_id=None)
            action_form.fields['action'].choices = choices
            
            if action_form.is_valid():
                action = action_form.cleaned_data['action']
                response = self.batchadmin_dispatch(request, changelist, action)
                if isinstance(response, HttpResponse):
                    return response
                else:
                    redirect_to = request.META.get('HTTP_REFERER') or "."
                    return HttpResponseRedirect(redirect_to)
        else:
            action_form = self.batch_action_form(auto_id=None)
            action_form.fields['action'].choices = choices
        context = {
            'batchadmin_action_form': action_form,
            'batchadmin_media': action_form.media,
            'batchadmin_on_top': self.actions_on_top,
            'batchadmin_on_bottom': self.actions_on_bottom
        }
        context.update(extra_context or {})
        return super(BatchModelAdmin, self).changelist_view(request, context)
