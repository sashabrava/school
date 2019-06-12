from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

def check_url(self, page, code=200, **kwargs):
    response = self.client.get(reverse(page,kwargs=kwargs)) 
    self.assertEqual(response.status_code, code)

class MainPageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='user@example.com', password='12345')

    def test_templates(self): 
        check_url(self, "main_pages:index")
        check_url(self, "main_pages:contacts")
        check_url(self, "main_pages:user-edit", 302)
        self.client.login(
                username='user', password='12345')
        check_url(self, "main_pages:user-edit")
        check_url(self, "main_pages:user-delete")
