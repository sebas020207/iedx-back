from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import *
# Register your models here.

admin.site.register(Info)


@admin.register(Administrator)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Custom info'), {
         'fields': ('name', 'last_name', 'address', 'phone', 'role', 'photo')}),
        (_('Personal info'), {'fields': ('first_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff',
                    'name', 'address', 'phone', 'role', 'photo')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
