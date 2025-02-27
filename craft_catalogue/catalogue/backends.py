# catalogue/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class UsernameAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)  # Only check username
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None