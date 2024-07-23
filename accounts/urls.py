# accounts/urls.py

from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
