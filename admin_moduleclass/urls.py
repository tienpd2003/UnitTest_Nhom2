from django.urls import path
from . import views

urlpatterns = [
    path('get-faculty/', views.get_faculty, name ='get_faculty_moduleclass'),
    path('get-department/<str:idFaculty>/', views.get_department, name ='get_department_moduleclass'),
    path('get-idCourse/', views.get_idCourse, name ='get_idCourse'),
    path('get-class/<str:idDepartment>/<str:idCourse>/', views.get_class, name ='get_class'),
    path('search-class/<str:input_value>/', views.get_search_class, name ='search_class'),
    path('get-list-module/<str:idClass>/', views.get_list_module, name ='get_list_module'),
    path('get-module-byidModule/<str:idModule>/', views.get_module_byidModule, name='get_module_byidModule'),
    path('get-room/',views.get_room, name='get_room'),
    path('get-semester/', views.get_semester, name='get_semester'),
    path('get-moduleclass/<str:idClass>/<idSemester>/', views.get_module_idClass_idSemester, name = 'get_moduleclass'),
    path('get-schedule-detail/<str:idClass>/<str:idModule>/', views.get_schedule_detail, name = 'get_schedule_detail'),
    path('delete-schedule/<str:idSMC>/', views.delete_schedule, name = 'delete_schedule'),
    path('save-moduleclass/<str:idClass>/<str:idModule>/<str:idSemester>/', views.save_moduleclass, name='save_moduleclass'),
    path('delete-moduleclass/<str:idClass>/<str:idModule>/', views.delete_moduleclass, name='delete_moduleclass'),
    path('check-moduleclass-exist/<str:idClass>/<str:idModule>/', views.check_moduleclass_exist, name='check_moduleclass_exist')
]