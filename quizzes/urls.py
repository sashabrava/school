from django.urls import path
from . import views


app_name = 'quizzes'
urlpatterns = [
path('quizzes/', views.quizzes, name='quizzes'),
path('quiz/upload', views.quiz_upload, name='quiz-upload'),
path('quiz/<int:pk>', views.quiz, name='quiz'),
path('quiz/<int:pk>/correct-replies', views.correct_replies, name='correct-replies'),
path('result/', views.result, name='result'),
path('quiz/edit/<int:pk>/', views.edit_quiz, name='edit-quiz'),
path('user/results', views.user_results, name='user-results'),
path('user/result/<int:pk>/', views.user_result, name='user-result'),
path('user/result/<int:pk>/pdf', views.UserResultPdf.as_view(), name='user-result-pdf'),
]
