from django.urls import path
from instagram.views import register_instagram_user

urlpatterns = [
   path('register_instagram_user', register_instagram_user, name='register_instagram_user'),
]