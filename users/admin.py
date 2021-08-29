from django.contrib import admin

from .models import UserVerifyToken


class UserVerifyTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserVerifyToken, UserVerifyTokenAdmin)
