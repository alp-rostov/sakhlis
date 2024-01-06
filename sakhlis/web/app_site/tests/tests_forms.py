from app_site.forms import *
from app_site.models import CITY_CHOICES

from sakhlis.web.app_site.tests.tests_models import Settings


class OrderFormTest(Settings):

    def test_renew_form_date_field_label(self):
        form = OrderForm()
        self.assertTrue(
                        form.fields['text_order'].label == 'Текст заказа' and
                        form.fields['customer_name'].label == 'Ваше имя' and
                        form.fields['customer_phone'].label == 'Телефон' and
                        form.fields['customer_telegram'].label == 'Телеграм' and
                        form.fields['address_city'].choices == CITY_CHOICES and
                        form.fields['address_street_app'].label == 'Улица' and
                        form.fields['address_num'].label == 'Номер дома'
                        )