from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class MainPageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='user@example.com', password='12345')

    def __check_url(self, page, code=200, **kwargs):
        response = self.client.get(reverse(page,kwargs=kwargs)) 
        self.assertEqual(response.status_code, code)    

    def test_templates(self): 
        self.__check_url("main_pages:index")
        self.__check_url("main_pages:contacts")
        self.__check_url("main_pages:user-edit", 302)
        self.client.login(
                username='user', password='12345')
        self.__check_url("main_pages:user-edit")
        self.__check_url("main_pages:user-delete")
