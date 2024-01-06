from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from app_site.models import *


class Settings(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_ = User.objects.create(username='User_test_unit')
        cls.user_.set_password('12345')
        cls.user_.save()
        cls.user = User.objects.get(username='User_test_unit')

        cls.order_ = OrderList.objects.create(customer_name="Ivan", customer_phone="999999999",
                                              customer_telegram='teleg-test', repairer_id=cls.user)
        cls.service_ = Service.objects.create(name='water tap installation', type='EL')
        cls.invoice = Invoice.objects.create(order_id=cls.order_, service_id=cls.service_, quantity=1, price=10, )
        cls.ord = OrderList.objects.get(customer_name="Ivan")
        cls.inv = Invoice.objects.get(order_id=cls.ord)
        cls.serv = Service.objects.get(name='water tap installation')

        cls.repaier = RepairerList.objects.filter(user=cls.user).exists()
        cls.repaier_=RepairerList.objects.filter(user=cls.user).first()
        cls.repaier_.phone='+999999999'
        cls.repaier_.save()


class ModelsTestCase(Settings):
    def test_repair_model(self):
        self.assertEqual(self.repaier_.phone, '+999999999')

    def test_validator_repair_model(self):
        repair = RepairerList(phone='+34346dfndfdfberdht erth ertd3464')
        with self.assertRaises(ValidationError):
            repair.full_clean()
            repair.save()

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
        self.assertEqual(self.user.username, 'User_test_unit')
        # self.assertEqual(self.repaier, True)



