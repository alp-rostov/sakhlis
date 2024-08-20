import os
import telebot
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import OrderList

@shared_task
def send_to_telegrambot(inst: int,TOKEN_:str, CHAT_ID_:str):
    """" send order`s information to telegram group"""
    instance = OrderList.objects.get(pk=inst)
    subject_ = f'<b>Order № {instance.pk} от {instance.time_in.strftime("%m/%d/%Y")}</b>'
    text = f'\n ' \
           f'Name: {instance.customer_id.customer_name} \n' \
           f'Phone: {instance.customer_id.phone} \n ' \
           f'Telegram: <a href = "https://t.me/{instance.customer_id.telegram}" >{instance.customer_id.telegram}</a> \n' \
           f'WhatsApp: <a href = "https://wa.me/{instance.customer_id.whatsapp}" >{instance.customer_id.whatsapp}</a> \n' \
           f'Address: {instance.apartment_id.address_street_app},{instance.apartment_id.address_num}, {instance.apartment_id.address_city}, \n' \
           f'{instance.text_order} \n' \

    bot = telebot.TeleBot( TOKEN_)
    bot.send_message(CHAT_ID_,  subject_+text, parse_mode='HTML')



@shared_task
def send_email(pk:int, username:str, email:str,):
    html_content = render_to_string(
        'emails/registration.html',
        {'pk': pk, 'username': username }
    )
    subject_ = f'User registration | sakhlis-remonti.ge'
    msg = EmailMultiAlternatives(
        subject=subject_,
        from_email='admin@sakhlis-remonti.ge',
        to=[email],
        )
    msg.attach_alternative(html_content, "text/html")  # add html

    msg.send()  # send email