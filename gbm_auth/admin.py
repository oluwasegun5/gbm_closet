from django.contrib import admin

from .models import AppUser as User


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)