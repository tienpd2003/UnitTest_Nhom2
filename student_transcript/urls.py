
from django.urls import path
from . import views


urlpatterns = [
    path('get-semester-std/<str:idStd>/', views.get_semester_std, name='student_get_semester'),
    path('get-transcript-semester/<str:idStd>/<str:semester>/', views.get_transcript_semester, name="student_get_transcript_semester"),

]