import os
import telebot
from celery import shared_task
from django.utils.encoding import force_str
from .models import OrderList, UserProfile



# @shared_task
def send_order_information(inst: int):
    TOKEN_ = force_str(os.environ.get('TOKEN'))
    CHAT_ID_ = force_str(os.environ.get('CHAT_ID'))
    """" send order`s information to telegram group"""
    instance = OrderList.objects.get(pk=inst)
    subject_ = f'<b>Заказ на работы № {instance.pk} от {instance.time_in.strftime("%m/%d/%Y")}</b>'
    text = f'\n ' \
           f'Name: {instance.customer_id.customer_name} \n' \
           f'Phone: {instance.customer_id.phone} \n ' \
           f'Telegram: <a href = "https://t.me/{instance.customer_id.telegram}" >{instance.customer_id.telegram}</a> \n' \
           f'WhatsApp: <a href = "https://wa.me/{instance.customer_id.whatsapp}" >{instance.customer_id.whatsapp}</a> \n' \
           f'Address: {instance.apartment_id.address_street_app},{instance.apartment_id.address_num}, {instance.apartment_id.address_city}, \n' \
           f'{instance.text_order} \n' \

    bot = telebot.TeleBot(TOKEN_)
    bot.send_message(CHAT_ID_,  subject_+text, parse_mode='HTML')
    print('fffffffffffffffffffffffffffff')
