"""
URL configuration for std_mng_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from course import views as course_views
from tuitionfee import views as tuitionfee_views
from login_std import views as login_std_views
from login_admin import views as login_admin_views
from admin_mngprofilestd import views as admin_mngprofilestd_views
from admin_moduleclass import views as admin_moduleclass_views
from admin_mngtranscript import views as admin_mngtranscript_views
from student_transcript import views as student_transcript_views
from schedule import views as schedule_views
from admin_mngnewsfeed import views as admin_mngnewsfeed_views




urlpatterns = [
    #superuser
    path('superuser/', admin.site.urls),
    #trang sinh vien
    path('', login_std_views.login_std, name='login_std'),
    path('profile/', login_std_views.profile_view, name='profile'),
    path('logout-std/', login_std_views.logout_std_view, name='logout_std'),
    path('change-password/', login_std_views.change_password_view, name='change_password'),
    path('change-password/', include('login_std.urls')),
    #trang admin
    path('admin/', login_admin_views.login_admin, name='login_admin'),
    path('logout-admin/', login_admin_views.logout_admin_view, name='logout_admin'),
    path('change-password-admin/', login_admin_views.change_password_admin_view, name='change_password_admin'),
    path('change-password-admin/', include('login_admin.urls')),
    #ket qua hoc tap
    path('transcript/', student_transcript_views.transcript_view, name='student_transcript'),
    path('transcript/', include('student_transcript.urls')),
    #dang ky hoc phan
    path('module-registration/', course_views.module_registration_view, name= 'module_registration'),
    path('module-registration/', include('course.urls')),
    #lich hoc
    path('schedule/', schedule_views.schedule_view, name= 'student_schedule'),
    path('schedule/', include('schedule.urls')),
    # trang quan tri vien
    path('admin-mngprofilestd', admin_mngprofilestd_views.admin_mngprofilestd , name = 'admin_mngprofilestd'),
    path('detail-profile-std/<str:idStd>/', admin_mngprofilestd_views.get_profile_detail, name = 'detail_profile_std'),
    path('get-faculty/', admin_mngprofilestd_views.get_faculty, name = 'get_faculty'),
    path('get-department/<str:idFaculty>/', admin_mngprofilestd_views.get_department, name = 'get_department'),
    path('get-idCourse/', admin_mngprofilestd_views.get_idCourse, name = 'get_idCourse'),
    path('get-class/<str:idDepartment>/', admin_mngprofilestd_views.get_class, name = 'get_class'),
    path('get-class-add-course/<str:idDepartment>/<str:idCourse>/', admin_mngprofilestd_views.get_class_add_course, name = 'get_class'),
    path('update-or-create-profile/', admin_mngprofilestd_views.update_or_create_profile, name = 'update_or_create_profile'),
    #quản lý lop mon hoc
    path('admin-moduleclass/', admin_moduleclass_views.admin_moduleclass, name = 'admin_moduleclass'),
    path('admin-moduleclass/', include('admin_moduleclass.urls')),
    #quan ly diem
    path('admin-mngtranscript/', admin_mngtranscript_views.admin_mngtranscript, name = 'admin_mngtranscript'),
    path('admin-mngtranscript/', include('admin_mngtranscript.urls')),
    #hoc phi
    path('tuitionfee/', tuitionfee_views.tuitionfee_view, name = 'tuitionfee'),
    path('tuitionfee/', include('tuitionfee.urls')),
    #quan ly tin tuc
    path('admin-mngnewsfeed/', admin_mngnewsfeed_views.admin_mngnewsfeed, name = 'admin_mngnewsfeed'),
    path('admin-mngnewsfeed/', include('admin_mngnewsfeed.urls')),
]