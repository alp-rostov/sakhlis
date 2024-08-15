import os
import telebot
from celery import shared_task

from .models import OrderList, UserProfile

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@shared_task
def send_order_information(inst: int):
    """" send order`s information to telegram group"""
    instance = OrderList.objects.get(pk=inst)
    subject_ = f'<b>Заказ на работы № {instance.pk} от {instance.time_in.strftime("%m/%d/%Y")}</b>'
    text = subject_ + f'\n ' \
                      f'Description: {instance.text_order} \n' \

    bot = telebot.TeleBot(TOKEN)
    bot.send_message(CHAT_ID, text, parse_mode='HTML')
