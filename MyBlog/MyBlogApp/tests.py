"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.test import TestCase, Client


class CreateBlogTestCase(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.my_user = User.objects.get(id=3)
        self.client = Client()

    def tearDown(self):
        self.my_user = None
        self.client = None

    def sign_in_first(self):
        login_successful = self.client.login(username=self.my_user.username, password="xx")
        self.assertTrue(login_successful)
        return login_successful

    def test_creation_from_is_not_reachable_if_not_signed_in(self):
        resp = self.client.get("/addblog/")
        self.assertEqual(resp.status_code, 302, "The user is redirected because he is not logged in")
        self.assertRedirects(resp, "/login/?next=/addblog/")

    def test_after_signed_in_user_redirected_to_creation_form(self):
        resp = self.client.post("/login/?next=/addblog/", {"username": self.my_user.username,
                                                           "password": "xx"})
        self.assertEqual(resp.status_code, 302, "The user is redirected")
        self.assertEqual(resp['Location'], 'http://testserver/addblog/')

    def test_if_user_logged_in_then_creation_form_sent(self):
        login_successful = self.sign_in_first()
        self.assertTrue(self.my_user.is_authenticated())
        self.assertTrue(login_successful)
        response = self.client.get("/addblog/")
        self.assertEqual(response['Location'], 'http://testserver/editblog/4')


class EditBlogTestCase(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.my_user = User.objects.get(id=3)
        self.client = Client()

    def tearDown(self):
        self.my_user = None
        self.client = None

    def sign_in_first(self):
        login_successful = self.client.login(username=self.my_user.username, password="xx")
        self.assertTrue(login_successful)
        return login_successful

    def test_edit_from_is_not_reachable_if_not_signed_in(self):
        resp = self.client.get("/editblog/1/")
        self.assertEqual(resp.status_code, 302, "The user is redirected because he is not logged in")
        self.assertRedirects(resp, "/login/?next=/editblog/1/")

    def test_after_signed_in_user_redirected_to_edit_form(self):
        resp = self.client.post("/login/?next=/editblog/1/", {"username": self.my_user.username,
                                                           "password": "xx"})
        self.assertEqual(resp.status_code, 302, "The user is redirected")
        self.assertEqual(resp['Location'], 'http://testserver/editblog/1/')
        self.assertRedirects(resp, "/editblog/1/")

    def test_if_user_logged_in_then_edit_form_sent_directly(self):
        login_successful = self.sign_in_first()
        self.assertTrue(self.my_user.is_authenticated())
        self.assertTrue(login_successful)
        response = self.client.get("/editblog/1/")
        self.assertTemplateUsed(response, "edit.html")
