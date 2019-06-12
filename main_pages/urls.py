from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'main_pages' 
urlpatterns = [
    path('', TemplateView.as_view(template_name="main_pages/index.html"), name='index'),
    path('contacts/', TemplateView.as_view(template_name="main_pages/contacts.html"), name='contacts'),
	path('user/edit/', views.edit_user, name='user-edit'),
    path('user/delete/', views.delete_user, name='user-delete'),
]