from django.urls import path
from . import views


urlpatterns = [
    path('get-search-class/<str:value>/', views.get_search_class, name="get_search_class"),
    path('get-list-module/<str:idClass>/', views.get_list_module, name="get_list_module"),
    path('get-list-std/<str:idClass>/<str:idModule>/', views.get_list_std, name="get_list_std"),
    path('upload-file-excel/<str:idClass>/<str:idModule>/<str:action>/', views.upload_file_excel, name="upload_file_excel"),
    path('get-profile-std/<str:idStd>/',views.get_profile_std, name="get_profile_std_transcript"),
    path('get-semester-std/<str:idStd>/', views.get_semester_std, name="get_semester_std_transcript"),
    path('get-transcript-semester/<str:idStd>/<str:semester>/', views.get_transcript_semester, name="get_transcript_semester_transcript"),
]