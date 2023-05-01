from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import OrderList, AREA_CHOICES
from geopy.geocoders import Nominatim
import telebot

TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
CHAT_ID = 5621399532


@receiver(post_save, sender=OrderList)
def send_post_new_order(instance, created, **kwargs):
    if created:
        geolocator = Nominatim(user_agent="app_site", )
        location = geolocator.geocode({'street': {instance.address_street_app}, 'city': 'Тбилиси'}, addressdetails=True)
        # определяем координаты по адресу
        map_ = ''
        if location:
            print((location.latitude, location.longitude))
            map_ = f'https://yandex.ru/maps/?pt={location.longitude},{location.latitude}&z=18&l=map'

        html_content = render_to_string('email.html',  {'instance': instance, })
        subject_ = f'Заказ на работы № {instance.pk} от {instance.time_in.strftime("%Y-%M-%d")}'
        from_ = 'alp-rostov@mail.ru'
        area = dict(AREA_CHOICES).get(instance.address_area)
        text = subject_ + f'\n ' \
                          f'ИМЯ: {instance.customer_name } \n' \
                          f'ТЕЛЕФОН: {instance.customer_phone } \n ' \
                          f'АДРЕС: {area},  {instance.address_street_app}, ' \
                          f'{instance.address_num} \n ' \
                          f'ОПИСАНИЕ ПРОБЛЕМЫ: {instance.text_order} \n' \
                          f'{map_}'

        msg = EmailMultiAlternatives(
            subject=subject_,
            body='',  # это то же, что и message
            from_email=from_,
            to=['alprostov.1982@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем письмо о новом заказе на почту

        bot = telebot.TeleBot(TOKEN)

        bot.send_message(CHAT_ID, text)  # направляем уведомление о новом заказе в телеграмм
