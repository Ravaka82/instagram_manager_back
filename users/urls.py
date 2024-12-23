from django.urls import path

from users.views import inscription, login




urlpatterns = [
    path('authentification', login, name='login'),
    path('inscription', inscription, name='inscription'),
    
]
