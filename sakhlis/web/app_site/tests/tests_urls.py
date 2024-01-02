from pprint import pprint


from django.test import TestCase


from sakhlis.web.app_site.tests.tests_models import Settings


class UrlTestCase(Settings):

    def testhomeurl(self):
        login = self.client.login(username='qqq', password='12345')
        response=self.client.get('/')
        self.assertEqual(str(response.context['user']), 'qqq')
        self.assertEqual(response.status_code, 200)

    def test404url(self):
        response = self.client.get('/error404/')
        self.assertEqual(response.status_code, 200)

    def testloginurl(self):
        response=self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def testlogouturl(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 301)

    def testregisterurl(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def teststaturl(self):
        response = self.client.get('/stat')
        self.assertEqual(response.status_code, 301)
        login = self.client.login(username='qqq', password='12345')
        response = self.client.get('/stat/')
        self.assertEqual(response.status_code, 200)
    def testlist_orderurl(self):
        response = self.client.get('/list_order')
        self.assertEqual(response.status_code, 302)
        login = self.client.login(username='qqq', password='12345')
        response = self.client.get('/list_order')
        self.assertEqual(response.status_code, 200)

    def testuserurl(self):
        response = self.client.get('/user/'+str(self.user.pk))
        self.assertEqual(response.status_code, 302)
        login = self.client.login(username='qqq', password='12345')
        response = self.client.get('/user/'+str(self.user.pk))
        self.assertEqual(response.status_code, 200)

