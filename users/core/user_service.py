from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserService:
    def register_user(self, username, email, password, **extra_fields):
      
        user = User.objects.create_user(username=username, email=email, password=password, **extra_fields)
        return user

    def find_user_by_username(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def find_user_by_id(self, user_id):
       
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None

    def remove_user(self, user_id):
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def authenticate_user(username, password):
      
        user = authenticate(username=username, password=password)
        return user
