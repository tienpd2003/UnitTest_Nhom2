from django.contrib import admin
from .models import *
from schedule.models import *

#đăng ký bảng học kỳ vào trang quản trị viên
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('idSemester', 'nameSemester','start_date','end_date')
    search_fields = ['idSemester', 'nameSemester','start_date','end_date']
    
admin.site.register(Semester, SemesterAdmin)



#đăng ký bảng môn học sinh viên vào trang quản trị
class Student_ModuleClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'module_class_display', 'idStd_display', 'process_grade', 'final_grade', 'overall_grade', 'overall_grade_4', 'overall_grade_text', 'is_pass')
    search_fields = ('id','module_class__module__idModule','idStd__idStd', 'process_grade', 'final_grade', 'overall_grade', 'overall_grade_4', 'overall_grade_text','is_pass')
  

    def module_class_display(self, obj):
        return obj.module_class.module.idModule
    module_class_display.short_description = 'Mã học phần'

    def idStd_display(self, obj):
        return obj.idStd.idStd
    idStd_display.short_description = 'MSSV'

    
admin.site.register(Student_ModuleClass, Student_ModuleClassAdmin)



#đăng ký bảng lớp môn học vào trang quản trị
class SessionScheduleInline(admin.TabularInline):
    model = ScheduleModuleClass
    extra = 1

class ModuleClassAdmin(admin.ModelAdmin):
    list_display = ('idModuleClass','module_display','idClass')
    search_fields = ('idModuleClass','module','idClass',)
    inlines = [SessionScheduleInline]

    def module_display(self, obj):
        return obj.module.idModule
    module_display.short_description = 'Mã học phần'


admin.site.register(ModuleClass, ModuleClassAdmin)



#đăng ký bảng danh sách môn học vào trang quản trị
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('idModule','nameModule','credits','department')
    search_fields = ('idModule','nameModule','credits','department__nameDepartment')
    autocomplete_fields =('department',)

admin.site.register(Module, ModuleAdmin)


#Lich dang ky hoc phan
class RegistrationScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'semester', 'idCourse', 'start_date', 'end_date')
    search_fields = ('id', 'semester', 'idCourse', 'start_date', 'end_date')

admin.site.register(RegistrationSchedule, RegistrationScheduleAdmin)
