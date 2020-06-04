from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.


class BlogUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlogUser, BlogUserAdmin)
