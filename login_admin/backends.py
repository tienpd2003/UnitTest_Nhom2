from django.contrib.auth.backends import ModelBackend
from .models import *


#backend login admin
class CustomAuthBackendAdmin(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user_admin = profile_admin.objects.get(idAdmin=username)
            if user_admin.check_custom_password(password):
                return user_admin
        except profile_admin.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return profile_admin.objects.get(pk=user_id)
        except profile_admin.DoesNotExist:
            return None