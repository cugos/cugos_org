"""
Utility functions for retrieving and generating forms for the
site-specific user profile model specified in the
``AUTH_PROFILE_MODULE`` setting.

"""

from django import forms
from django.conf import settings
from django.db.models import get_model
from django.forms.util import ValidationError
from django.contrib.auth.models import User

from django.contrib.auth.models import SiteProfileNotAvailable


def get_profile_model():
    """
    Return the model class for the currently-active user profile
    model, as defined by the ``AUTH_PROFILE_MODULE`` setting. If that
    setting is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    if (not hasattr(settings, 'AUTH_PROFILE_MODULE')) or \
           (not settings.AUTH_PROFILE_MODULE):
        raise SiteProfileNotAvailable
    profile_mod = get_model(*settings.AUTH_PROFILE_MODULE.split('.'))
    if profile_mod is None:
        raise SiteProfileNotAvailable
    return profile_mod

attrs_dict = { 'class': 'required' }

def get_profile_form():
    """
    Return a form class (a subclass of the default ``ModelForm``)
    suitable for creating/editing instances of the site-specific user
    profile model, as defined by the ``AUTH_PROFILE_MODULE``
    setting. If that setting is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    profile_mod = get_profile_model()
    class _ProfileForm(forms.ModelForm):
        email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75)),
            label='Provide new email',
            required=False)
        
        class Meta:
            model = profile_mod
            exclude = ('user','uid')

        def clean(self):
            # note: geometry is excluded so we pull from 'data' rather than 'cleaned_data'
            email = self.cleaned_data.get('email')
            if email:
              #import pdb;pdb.set_trace()
              #user = User.objects.get(username)
              user = self.instance.user
              user.email = email
              user.save()
            return self.cleaned_data
        
    return _ProfileForm
