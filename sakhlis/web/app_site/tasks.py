import telebot
from celery import shared_task
from django.template.loader import render_to_string
from geopy.geocoders import Nominatim
from telebot import types

from .models import OrderList, RepairerList

TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
CHAT_ID = 5621399532


@shared_task
def send_order_information(inst):
    instance = OrderList.objects.get(pk=inst)
    geolocator = Nominatim(user_agent="app_site", )
    location = geolocator.geocode({'street': {instance.address_street_app}, 'city': 'Тбилиси'}, addressdetails=True)
    # определяем координаты по адресу
    map_ = ''
    if location:
        print((location.latitude, location.longitude))
        map_ = f'https://yandex.ru/maps/?pt={location.longitude},{location.latitude}&z=18&l=map'

    # создание кнопок в телеграмм
    repairer = RepairerList.objects.all().values('pk', 's_name')
    keyboard = types.InlineKeyboardMarkup()
    button = []
    for i in repairer:
        url_ = f'http://127.0.0.1:8000/add?pk_order=' \
               f'{instance.pk}&pk_repairer={i.get("pk")}'       # link to add repaier_id in order
        button.append(types.InlineKeyboardButton(text=i.get("s_name"), url=url_))
    keyboard.add(*button)

    # html_content = render_to_string('email.html', {'instance': instance, })
    subject_ = f'<b>Заказ на работы № {instance.pk} от {instance.time_in.strftime("%m/%d/%Y")}</b>'
    # from_ = 'alp-rostov@mail.ru'
    text = subject_ + f'\n ' \
                      f'ИМЯ: {instance.customer_name} \n' \
                      f'ТЕЛЕФОН: {instance.customer_phone} \n ' \
                      f'АДРЕС: {instance.address_street_app}, ' \
                      f'{instance.address_num} \n ' \
                      f'ОПИСАНИЕ ПРОБЛЕМЫ: {instance.text_order} \n' \
                      f'{map_}  \n' \
                      f'<b>ОТПРАВИТЬ ЗАКАЗ МАСТЕРУ:</b>' \

    # msg = EmailMultiAlternatives(
    #     subject=subject_,
    #     body='',  # это то же, что и message
    #     from_email=from_,
    #     to=['alprostov.1982@gmail.com'],  # это то же, что и recipients_list
    # )
    # msg.attach_alternative(html_content, "text/html")  # добавляем html

    # msg.send()  # отсылаем письмо о новом заказе на почту

    bot = telebot.TeleBot(TOKEN)

    bot.send_message(CHAT_ID, text, reply_markup=keyboard,  parse_mode='HTML')
