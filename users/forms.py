from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AuthenticationLDAPForm(AuthenticationForm):

    domain = forms.ChoiceField(choices=settings.DOMAIN_CHOICES, label=_('Domain'))
    is_superuser = forms.BooleanField(required=False, label=_('Superuser'))

    error_messages = {
        'invalid_login': _('Please enter a correct domain, username and password'),
        'unconfirmed': _('This user is not confirmed')
    }

    def clean(self):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')
        domain = self.cleaned_data.get('domain').lower()
        is_superuser = self.cleaned_data.get('is_superuser')

        if username and domain and password:
            if is_superuser:
                domain = settings.DOMAIN_SUPERUSER
            self.user_cache = authenticate(
                self.request, username=username, domain=domain, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_confirmed:
            raise ValidationError(
                self.error_messages['unconfirmed'],
                code='unconfirmed',
            )
