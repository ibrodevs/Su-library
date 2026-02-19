from django.contrib import admin
from .models import User
from unfold.admin import ModelAdmin


class UserAdmin(ModelAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'group', 'course')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

    exclude = ('last_login', 'groups', 'user_permissions', 'date_joined')

    list_display = ('email', 'first_name', 'last_name', 'group', 'course', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'group', 'course')
    search_fields = ('email', 'first_name', 'last_name', 'group')

admin.site.register(User, UserAdmin)
