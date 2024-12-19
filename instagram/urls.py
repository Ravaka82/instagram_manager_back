from django.urls import path

from instagram.views import add_instagram_account


urlpatterns = [
    ##path('followers/', get_followers, name='get_followers'),
    path('add-instagram-account', add_instagram_account, name='add_instagram_account'),
]