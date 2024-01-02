from django.contrib.auth.models import User
from django.test import TestCase
from app_site.models import *


class Settings(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.order_ = OrderList.objects.create(customer_name="Ivan", customer_phone="999999999",
                                              customer_telegram='teleg-test')
        cls.service_ = Service.objects.create(name='water tap installation', type='EL')
        cls.invoice = Invoice.objects.create(order_id=cls.order_, service_id=cls.service_, quantity=1, price=10, )
        cls.ord = OrderList.objects.get(customer_name="Ivan")
        cls.inv = Invoice.objects.get(order_id=cls.ord)
        cls.serv = Service.objects.get(name='water tap installation')

        cls.user_ = User.objects.create(username='qqq')
        cls.user_.set_password('12345')
        cls.user_.save()

        cls.user = User.objects.get(username='qqq')
        cls.repaier = RepairerList.objects.filter(user=cls.user).exists()




class ModelsTestCase(Settings):


    def test_order_model(self):
        self.assertEqual(self.ord.customer_name, 'Ivan')
        self.assertEqual(self.ord.customer_phone, '999999999')
        self.assertEqual(self.ord.customer_telegram, 'teleg-test')
        self.assertEqual(self.ord.address_city, 'TB')
        self.assertEqual(self.ord.order_status, 'BEG')

    def test_invoice_model(self):
        self.assertEqual(self.inv.service_id.name, 'water tap installation')
        self.assertEqual(self.ord.invoice_set.all()[0].quantity, 1)
        self.assertEqual(self.ord.invoice_set.all()[0].price, 10)

    def test_service_model(self):
        self.assertEqual(self.serv.type, 'EL')

    def test_user(self):
        self.assertEqual(self.user.username, 'qqq')
        self.assertEqual(self.repaier, True)



