import os
import telebot

from celery import shared_task
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import OrderList, Repairer
from .utils import get_telegram_button, Location

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@shared_task
def task_save_location_(inst: int):
    order = get_object_or_404(OrderList, pk=inst)
    Location(order).save_location()

@shared_task
def send_order_information(inst: int):
    """" send order`s information to telegram group"""
    instance = OrderList.objects.get(pk=inst)
    repairer = User.objects.all().values_list('pk', 'username')
    subject_ = f'<b>Заказ на работы № {instance.pk} от {instance.time_in.strftime("%m/%d/%Y")}</b>'
    map_= Location(instance).print_yandex_location()
    text = subject_ + f'\n ' \
                      f'NAME: {instance.customer_name} \n' \
                      f'PHONE: {instance.customer_phone} \n ' \
                      f'TELEGRAM: <a href = "https://t.me/{instance.customer_telegram}" >{instance.customer_telegram}</a> \n' \
                      f'ADDRESS: {instance.address_street_app}, ' \
                      f'{instance.address_num} \n ' \
                      f'Description: {instance.text_order} \n' \
                      f'{map_}  \n' \
                      f'<b>Send a request to the master:</b>' \

    bot = telebot.TeleBot(TOKEN)
    bot.send_message(CHAT_ID, text, reply_markup=get_telegram_button(repairer, instance.pk),  parse_mode='HTML')





