# authentication_backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        user = UserModel.objects.filter(Q(email=username) | Q(username=username)).first()

        if user and user.check_password(password):
            return user

        return None
