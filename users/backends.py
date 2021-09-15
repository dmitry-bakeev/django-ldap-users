import ldap

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class DomainModelBackend(ModelBackend):

    def authenticate(self, request, username=None, domain=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or domain is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(
                domain + settings.SEPARATE_CHARACTER + username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class LDAPModelBackend(ModelBackend):

    def _get_user(self, **kwargs):
        try:
            return UserModel.objects.get(**kwargs)
        except UserModel.DoesNotExist:
            return

    def _get_ldap_user_by_username(self, username, dn):
        try:
            search_scope = ldap.SCOPE_SUBTREE
            retrieve_attributes = None
            search_filter = "samaccountname=" + username
            result_id = self.connection.search(dn, search_scope, search_filter, retrieve_attributes)
            _, result_data = self.connection.result(result_id, 0)
            return result_data[0][1]

        except Exception:
            return {}

    def authenticate(self, request, username=None, password=None, domain=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or domain is None or password is None:
            return

        if domain not in settings.AUTH_LDAP_SERVERS:
            return

        ldap.set_option(ldap.OPT_REFERRALS, 0)

        try:
            self.connection = ldap.initialize('ldap://' + settings.AUTH_LDAP_SERVERS[domain]['URI'])
            self.connection.simple_bind_s(username + '@' + settings.AUTH_LDAP_SERVERS[domain]['DOMAIN'], password)
        except Exception:
            self.connection.unbind_s()
            return

        full_name = '{}{}{}'.format(domain, settings.SEPARATE_CHARACTER, username)
        user = self._get_user(username=full_name)

        if user is None:
            user = UserModel(username=full_name, password='', domain=domain)
            ldap_user = self._get_ldap_user_by_username(username=username, dn=settings.AUTH_LDAP_SERVERS[domain]['DN'])

            if ldap_user:
                try:
                    user.first_name = ldap_user['givenName'][0].decode('utf8')
                    user.last_name = ldap_user['sn'][0].decode('utf8')
                    user.email = ldap_user['mail'][0].decode('utf8')
                except Exception:
                    pass

            if settings.AUTO_CONFIRM_USER:
                user.is_confirmed = True

            user.save()

        self.connection.unbind_s()

        return user
