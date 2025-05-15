from django.contrib.auth.backends import ModelBackend
from .models import *


#backend login std
class CustomAuthBackendStd(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user_std = profile_std.objects.get(idStd=username)
            print(user_std)
            if user_std.check_custom_password(password):
                return user_std
        except profile_std.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return profile_std.objects.get(pk=user_id)
        except profile_std.DoesNotExist:
            return None