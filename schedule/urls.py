
from django.urls import path
from . import views


urlpatterns = [
    path('get-schedule/<str:idStd>/', views.get_moduleclass_schedule, name = 'get_schedule_student'),
]