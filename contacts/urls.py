# contacts/urls.py

from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.list_contacts, name='list_contacts'),
    path('logout/', views.logout_user, name='logout'),
    path('create/', views.create_contact, name='create_contact'),
    path('<int:pk>/edit/', views.edit_contact, name='edit_contact'),
    path('<int:pk>/delete/', views.delete_contact, name='delete_contact'),
    path('ajax/search/', views.ajax_search_contacts, name='ajax_search_contacts'),
]
