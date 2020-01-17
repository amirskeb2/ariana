from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser


class MyUserAdmin(UserAdmin):
    list_display = ('phone_number', 'email', 'last_login', 'is_staff', 'is_admin',)
    search_fields = ('phone_number', 'email', 'last_name')
    readonly_fields = ('last_login', 'date_joined')

    filter_horizontal = ()
    list_filter = ('is_staff',)
    fieldsets = ()


admin.site.register(MyUser, MyUserAdmin)

