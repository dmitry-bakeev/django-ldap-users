from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


class UserWithDomainAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'domain',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('role', 'is_confirmed',)}),
        ('Important dates', {'fields': ('created_at',)}),
    )

    list_filter = ()
    filter_horizontal = ()

    readonly_fields = (
        'username',
        'domain',
        'first_name',
        'last_name',
        'email',
        'created_at',
    )

    def has_add_permission(self, *args, **kwargs):
        return None


admin.site.register(User, UserWithDomainAdmin)

# Hide standart model Group in admin panel
admin.site.unregister(Group)
