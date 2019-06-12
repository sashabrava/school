from django.test import TestCase
from main_pages.tests import check_url
from .models import *

class NewsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Post.objects.create()

    def test_templates(self): 
        check_url(self, "news:news-list", 200)
        check_url(self, "news:news", 200, pk=1)