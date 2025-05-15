from django.contrib import admin
from .models import *


# Register your models here.
class tuitionfeeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in tuitionfee._meta.get_fields()]
    search_fields = ['idStd__idStd', 'idStd__nameStd',]

admin.site.register(tuitionfee, tuitionfeeAdmin)



class tuitionfee_scaleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in tuitionfee_scale._meta.get_fields()]
    search_fields = ['idSemester__idSemester',]
    autocomplete_fields = ['idSemester',]

admin.site.register(tuitionfee_scale, tuitionfee_scaleAdmin)