from django.urls import path
from . import views


urlpatterns = [
    path('change-password-admin/', views.change_password_admin),
]