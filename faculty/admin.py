from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


#tùy chỉnh giao diện của bảng Khoa trong admin
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('idFaculty','nameFaculty')
    search_fields = ('idFaculty', 'nameFaculty',)
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Faculty, FacultyAdmin)


#tùy chỉnh giao diện của bảng Ngành trong admin
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('idDepartment', 'nameDepartment', 'faculty')
    search_fields = ('idDepartment', 'faculty__nameFaculty', 'faculty__idFaculty', 'nameDepartment')
    autocomplete_fields = ('faculty',)
    

admin.site.register(Department, DepartmentAdmin)


#tùy chỉnh giao diện của bảng lớp trong Khoa
class FacultyClassesAdmin(admin.ModelAdmin):
     list_display = ('idClass', 'department','idCourse')
     search_fields = ('idClass', 'department__nameDepartment','idCourse__idCourse','view_students')
     autocomplete_fields = ('department','idCourse')



admin.site.register(FacultyClasses, FacultyClassesAdmin)


#Niên khóa
class idCourseAdmin(admin.ModelAdmin):
    list_display = ('idCourse', 'nameCourse')
    search_fields = ('idCourse', 'nameCourse')

admin.site.register(idCourse, idCourseAdmin)