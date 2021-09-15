from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/login/', RedirectView.as_view(pattern_name='users:login')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns = static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT) + urlpatterns
