from django.urls import path
from . import views


app_name = 'quizzes'
urlpatterns = [
path('', views.quizzes, name='quizzes'),
path('upload', views.quiz_upload, name='quiz-upload'),
path('<int:pk>', views.quiz, name='quiz'),
path('<int:pk>/correct-replies', views.correct_replies, name='correct-replies'),
path('result/', views.result, name='result'),
path('edit/<int:pk>/', views.edit_quiz, name='edit-quiz'),
path('user/results', views.user_results, name='user-results'),
path('admin/results', views.admin_results, name='admin-results'),
path('admin/results/api', views.AdminResultsApi.as_view(), name='admin-results-api'),
path('user/result/<int:pk>/', views.user_result, name='user-result'),
]
