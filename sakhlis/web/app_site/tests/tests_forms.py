from app_site.forms import *

from app_site.forms import OrderForm

from app_site.models import OrderList
from sakhlis.web.app_site.tests.tests_models import Settings


class OrderFormTest(Settings):

    def test_renew_form_date_field_label(self):
        count_of_order_before = OrderList.objects.count()
        data={'text_order':'test text of order', 'customer_name':'Sergei', 'customer_phone':'+995555555555','address_city':'TB' }
        not_valid_data = {'text_order': '', 'customer_name': '', 'customer_phone': '', 'address_city': ''}
        form = OrderForm(data)
        b=form.save()

        count_of_order_after = OrderList.objects.count()
        form_check_valid = OrderForm(not_valid_data)
        self.assertFalse(form_check_valid.is_valid())
        self.assertEqual(b.customer_phone, '995555555555')
        self.assertTrue(count_of_order_before == count_of_order_after-1)
