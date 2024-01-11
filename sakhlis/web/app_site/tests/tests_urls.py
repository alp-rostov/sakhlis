from app_site.models import OrderList
from sakhlis.web.app_site.tests.tests_models import Settings


class UrlTestCase(Settings):

    def test_home_url(self):
        data = {'text_order': 'test text of order', 'customer_name': 'Sergei', 'customer_phone': '+995555555555',
                'address_city': 'TB'}
        # without login:
            # check GET
        response=self.client.get('/')
        self.assertEqual(response.status_code, 200)
            # check POST
        response = self.client.post('/', data)
        chek_post = OrderList.objects.get(text_order="test text of order")
        self.assertEqual(chek_post.customer_name, 'Sergei')
        self.assertEqual(chek_post.repairer_id, None)
        OrderList.objects.filter(text_order="test text of order").delete()

        # with login
            # check GET
        login = self.client.login(username='User_test_unit', password='12345')
        response = self.client.get('/')
        self.assertTrue(login)
        self.assertEqual(str(response.context['user']), 'User_test_unit')
        self.assertIn('User_test_unit', response.content.decode())
            # check POST
        response = self.client.post('/', data)
        chek_post = OrderList.objects.get(text_order="test text of order")
        self.assertEqual(chek_post.customer_name, 'Sergei')
        self.assertEqual(chek_post.repairer_id.username, 'User_test_unit')
        OrderList.objects.filter(text_order="test text of order").delete()

            # check GET with wrong login:
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
