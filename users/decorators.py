import urllib

from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse


def role_required(*roles):

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                query = urllib.parse.urlencode({'next': request.path})
                return redirect(reverse(settings.LOGIN_URL) + '?' + query)
        return wrapper
    return decorator
