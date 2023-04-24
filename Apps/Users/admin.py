from django.contrib import admin
from Apps.Users.models import User
from Apps.Users.forms import UserForm, UpdateUserForm


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'is_staff', 'is_superuser']
    list_display_links = ['first_name']
    list_editable = ['is_staff', 'is_superuser']


admin.site.register(User, UserAdmin)
