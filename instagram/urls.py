from django.urls import path
from instagram.views import authenticate_instagram_user

urlpatterns = [
   path('authenticate_instagram_user', authenticate_instagram_user, name='authenticate_instagram_user'),
]