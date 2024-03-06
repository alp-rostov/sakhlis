from app_site.forms import *

from app_site.forms import OrderForm, InvoiceForm

from app_site.models import OrderList, Invoice
from sakhlis.web.app_site.tests.tests_models import Settings


class FormTest(Settings):

    def test_orderform(self):
        count_of_order_before = OrderList.objects.count()
        not_valid_data = {'text_order': '', 'customer_name': '', 'customer_phone': '', 'address_city': ''}
        form = OrderForm(self.data)
        b=form.save()

        count_of_order_after = OrderList.objects.count()
        form_check_valid = OrderForm(not_valid_data)
        self.assertFalse(form_check_valid.is_valid())
        self.assertEqual(b.customer_phone, '995555555555')
        self.assertTrue(count_of_order_before == count_of_order_after-1)

    def test_invoiceform(self):

        data = {'service_id': self.serv, 'order_id': self.ord, 'quantity_type': 'SV', 'quantity': 4, 'price':50}
        not_valid_data = {'service_id': self.serv, 'order_id': self.ord, 'quantity_type': 'SV', 'quantity': 'one', 'price':'ten'}

        count_of_invoice_before = Invoice.objects.count()
        form = InvoiceForm(data)
        b = form.save()
        count_of_invoice_after = Invoice.objects.count()

        form_check_valid = InvoiceForm(not_valid_data)
        self.assertFalse(form_check_valid.is_valid())
        self.assertEqual(b.price*b.quantity, 200)
        self.assertTrue(count_of_invoice_before == count_of_invoice_after-1)