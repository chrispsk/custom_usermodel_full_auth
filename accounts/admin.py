from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from . import models


class UserAdmin(BaseUserAdmin):
    ordering = ('username', 'email',)
    list_display = ('email', 'name', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('name','zipcode',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active',)}),
        ('Important dates', {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'username',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.ActivationKey)
admin.site.unregister(Group)
