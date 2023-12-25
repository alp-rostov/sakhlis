from django.test import TestCase

from .models import *
class OrderListTestCase(TestCase):
    def setUp(self):
        order_=OrderList.objects.create(customer_name="Ivan", customer_phone="999999999", customer_telegram='teleg-test')
        service_=Service.objects.create(name='Монтаж крана', type='EL')
        Invoice.objects.create(order_id=order_, service_id=service_, quantity=1, price=10, )


    def test_order_list(self):
        """_________________________________________________"""
        ord = OrderList.objects.get(customer_name="Ivan")
        inv= Invoice.objects.get(order_id=ord)

        self.assertEqual(ord.customer_name, 'Ivan')
        self.assertEqual(ord.customer_phone, '999999999')
        self.assertEqual(ord.customer_telegram, 'teleg-test')
        self.assertEqual(ord.address_city, 'TB')
        self.assertEqual(ord.order_status, 'BEG')

        self.assertEqual(inv.quantity, 1)
        self.assertEqual(inv.price, 10)
        self.assertEqual(inv.service_id.type, 'EL')

        self.assertEqual(Invoice.objects.get(service_id=ord.services.all()[0]).price, 10)
        self.assertEqual(ord.invoice_set.all()[0].quantity, 1)