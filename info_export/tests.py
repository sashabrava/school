from django.test import TestCase
from main_pages.tests import check_url
from django.contrib.auth.models import User
from quizzes.models import Quiz
from django.http import JsonResponse
from .tasks import async_quiz_docx
class InfoExportViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        Quiz.objects.create()

    def test_templates(self): 
        self.client.login(
                username='admin', password='admin')
        response = check_url(self, "info_export:quiz-docx", 200, pk=1)
        print (response.json()["task_id"])
        async_quiz_docx.AsyncResult(response.json()["task_id"]).get(timeout=5)
        self.client.logout()