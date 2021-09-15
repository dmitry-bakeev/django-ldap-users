from django.contrib.auth.views import LoginView

from .forms import AuthenticationLDAPForm


class LoginLDAPView(LoginView):
    template_name = 'users/login-ldap-form.html'
    form_class = AuthenticationLDAPForm
