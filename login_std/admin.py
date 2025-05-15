from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class profile_stdAdmin(admin.ModelAdmin):
    list_display = ('idStd', 'nameStd','idClass',)
    search_fields = ('idStd', 'nameStd','idClass__idClass',)
    autocomplete_fields = ('idClass',)

admin.site.register(profile_std, profile_stdAdmin)
admin.site.site_header = "Quản lý sinh viên"
