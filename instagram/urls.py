from django.urls import path
from instagram.views import register_instagram_user,get_all_instagram_user,register_master_account,update_instagram_user




urlpatterns = [
   path('register_instagram_user', register_instagram_user, name='register_instagram_user'),
   path('get_all_instagram_user', get_all_instagram_user, name='get_all_instagram_user'),
   path('register_master_account',register_master_account, name='register_master_account'),
   path('update_instagram_user/<str:username>', update_instagram_user, name='update_instagram_user'),
]