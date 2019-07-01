from django.urls import path
from . import views


app_name = 'info_export'
urlpatterns = [
    path('user/result/<int:pk>/pdf', views.UserResultPdf.as_view(), name='user-result-pdf'),
    path('quiz/<int:pk>/docx', views.generate_quiz_docx, name='quiz-docx'),
    path('download/<str:task_id>', views.get_async_file, name='get-async-file'),
    path('status/<str:task_id>', views.get_async_task_status, name='get-async-task-status'),
]