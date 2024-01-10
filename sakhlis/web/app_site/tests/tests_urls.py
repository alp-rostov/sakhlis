
from sakhlis.web.app_site.tests.tests_models import Settings


class UrlTestCase(Settings):

    def test_home_url(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('User_test_unit', response.content.decode())

        login = self.client.login(username='User_test_unit', password='12345')
        response = self.client.get('/')
        self.assertTrue(login)
        self.assertEqual(str(response.context['user']), 'User_test_unit')
        self.assertIn('User_test_unit', response.content.decode())

        login = self.client.login(username='User_test_unit', password='wrong_password')
        self.assertFalse(login)

    def test_stat_url(self):
        response = self.client.get('/stat')
        self.assertEqual(response.status_code, 301)
        login = self.client.login(username='User_test_unit', password='12345')
        response = self.client.get('/stat/')
        self.assertIn('User_test_unit', response.content.decode())
        self.assertEqual(response.status_code, 200)
    def test_list_order_url(self):
        response = self.client.get('/list_order')
        self.assertEqual(response.status_code, 302)

        login = self.client.login(username='User_test_unit', password='12345')
        response = self.client.get('/list_order')
        self.assertIn('User_test_unit', response.content.decode())
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/list_order/'+str(self.ord.pk))
        self.assertIn('Заявка № '+str(self.ord.pk), response.content.decode())
        self.assertEqual(response.status_code, 200)

    def test_user_url(self):
        response = self.client.get('/user/'+str(self.user_.pk))
        self.assertEqual(response.status_code, 302)

        login = self.client.login(username='User_test_unit', password='12345')
        response = self.client.get('/user/'+str(self.user_.pk))
        self.assertIn('User_test_unit', response.content.decode())
        self.assertEqual(response.status_code, 200)


    def test_404_url(self):
        response = self.client.get('/error404/')
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response=self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 301)

    def test_register_url(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)


    def test_user_url(self):
        response = self.client.get('/user/'+str(self.user.pk))
        self.assertEqual(response.status_code, 302)

        login = self.client.login(username='User_test_unit', password='12345')
        response = self.client.get('/user/'+str(self.user.pk))
        self.assertIn('Выполнено заказов', response.content.decode())
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/user/164511456454154')
        self.assertEqual(response.status_code, 400)

    def test_ordersearch_url(self):
        login = self.client.login(username='User_test_unit', password='12345')
        response = self.client.get('/ordersearch/')
        self.assertEqual(response.status_code, 200)
