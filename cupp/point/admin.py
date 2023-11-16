from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Point

admin.site.register(Point)
admin.site.unregister(User)


@admin.register(User)
class CUPPUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'groups'),
        }),
    )
    list_display = ('username', 'first_name', 'last_login')
    list_filter = ('is_active', 'groups')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(username='su')
