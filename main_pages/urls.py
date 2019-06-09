from django.urls import path

from . import views
app_name = 'main_pages' 
urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
	path('user/edit/', views.edit_user, name='user-edit'),
    path('user/delete/', views.delete_user, name='user-delete'),
]