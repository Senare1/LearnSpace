from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email_or_phone=None, teacher_register=None, password=None, **kwargs):
        if (email_or_phone is None and teacher_register is None) or password is None:
            return None

        try:
            if email_or_phone:
                # Authentication for learner
                user = None
                if '@' in email_or_phone:
                    user = User.objects.get(learner_email=email_or_phone)
                else:
                    user = User.objects.get(learner_phone=email_or_phone)
                
                if user and user.check_password(password):
                    return user
            elif teacher_register:
                # Authentication for teacher
                user = User.objects.get(teacher_register=teacher_register)
                
                if user and user.check_password(password):
                    return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
