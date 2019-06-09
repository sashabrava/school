from django.urls import path

from . import views
app_name = 'news' 
urlpatterns = [
    path('', views.page_posts, name='news-list'),
    path('<int:pk>/', views.post, name='news'),
]
