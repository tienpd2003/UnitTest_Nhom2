from django.contrib import admin
from .models import *


class ClassRoomAdmin(admin.ModelAdmin):
    list_display= ['idClassRoom','nameClassRoom']
    search_fields=['idClassRoom','nameClassRoom']

admin.site.register(ClassRoom, ClassRoomAdmin)

class ScheduleModuleClassAdmin(admin.ModelAdmin):
    list_display= ['idSMC', 'idModuleClass', 'days_of_week','period_start' ,'periods_count', 'start_date','end_date', 'class_room']
    search_fields= ['idSMC', 'idModuleClass', 'days_of_week','period_start' ,'periods_count', 'start_date', 'class_room']
admin.site.register(ScheduleModuleClass, ScheduleModuleClassAdmin)

class ScheduleFinalExamAdmin(admin.ModelAdmin):
    list_display = ['idSFE', 'idModuleClass', 'date_exam', 'period_start','class_room']
    search_fields = ['idSFE', 'idModuleClass', 'date_exam', 'period_start','class_room']
admin.site.register(ScheduleFinalExam, ScheduleFinalExamAdmin)

