import telebot
from celery import shared_task
from telebot import types
from .models import OrderList, RepairerList
from .utils import set_coordinates_address, add_telegram_button

TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
CHAT_ID = 5621399532


@shared_task
def send_order_information(inst):
    instance = OrderList.objects.get(pk=inst)
    repairer = RepairerList.objects.all().values_list('pk', 's_name')

    map_ = set_coordinates_address(instance.address_street_app, 'Тбилиси')
    subject_ = f'<b>Заказ на работы № {instance.pk} от {instance.time_in.strftime("%m/%d/%Y")}</b>'
    text = subject_ + f'\n ' \
                      f'ИМЯ: {instance.customer_name} \n' \
                      f'ТЕЛЕФОН: {instance.customer_phone} \n ' \
                      f'АДРЕС: {instance.address_street_app}, ' \
                      f'{instance.address_num} \n ' \
                      f'ОПИСАНИЕ ПРОБЛЕМЫ: {instance.text_order} \n' \
                      f'{map_}  \n' \
                      f'<b>ОТПРАВИТЬ ЗАКАЗ МАСТЕРУ:</b>' \


    bot = telebot.TeleBot(TOKEN)
    bot.send_message(CHAT_ID, text, reply_markup=add_telegram_button(repairer, instance.pk),  parse_mode='HTML')
