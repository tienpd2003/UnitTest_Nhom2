from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

class profile_adminAdmin(admin.ModelAdmin):
    list_display = [field.name for field in profile_admin._meta.get_fields()] 
    search_fields = [field.name for field in profile_admin._meta.get_fields()]

admin.site.register(profile_admin, profile_adminAdmin)  
admin.site.unregister(Group)