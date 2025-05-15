

from django.urls import path
from . import views


urlpatterns = [
    path('change-password-std/', views.change_password)
]