import os
import telebot
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .models import OrderList, UserProfile


@shared_task
def send_to_telegrambot(inst: int):
    # TOKEN_ = os.environ.get("TOKEN")
    # CHAT_ID_ = os.environ.get("CHAT_ID")
    TOKEN_ = '********'
    CHAT_ID_ = '****************'

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

    bot = telebot.TeleBot(TOKEN_)
    bot.send_message(CHAT_ID_,  subject_+text, parse_mode='HTML')



@shared_task
def send_email(email:str='', subject_:str=f'sakhlis-remonti.ge', template_name_:str = 'emails/registration.html', context_:dict={}):
    user_ = User.objects.get(pk=context_['pk'])
    token=UserProfile.objects.get(user=user_).customer_name
    context_['token'] = str(token)
    html_content = render_to_string(
        template_name=template_name_,
        context=context_
    )
    msg = EmailMultiAlternatives(
        subject=subject_,
        from_email='admin@sakhlis-remonti.ge',
        to=[email],
        )
    msg.attach_alternative(html_content, "text/html")
    msg.send()  # send email