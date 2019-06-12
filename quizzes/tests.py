from django.test import TestCase, Client
from main_pages.tests import check_url
from .models import *
import os
class QuizzesViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Quiz.objects.create()
	
    def test_templates(self): 
        check_url(self, "quizzes:quizzes")
        check_url(self, "quizzes:quiz", 200, pk=1)
        c = Client()
        with open(os.path.dirname(__file__) + "/../1.xml") as fp:
            response = c.post("/quizzes/upload", {'myfile': fp})
            Quiz.objects.get(pk=2)