from django.contrib import admin
from .models import *

# Register your models here.
class newsfeedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in newsfeed._meta.get_fields()]
    search_fields = ('title', 'post_date','is_hidden',)

admin.site.register(newsfeed, newsfeedAdmin)
