import telebot
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import OrderList, RepairerList
from .utils import set_coordinates_address, add_telegram_button

TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
CHAT_ID = 5621399532


@shared_task
def send_order_information(inst):
    """" send order`s information to telegram group"""
    instance = OrderList.objects.get(pk=inst)
    repairer = RepairerList.objects.all().values_list('pk', 'phone')

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


@shared_task
def send_email_after_registration(inst):
    """" send welcome letter to repairman after registration """
    inst_ = User.objects.get(pk=inst)

    html_content = render_to_string(
        'email_registration.html',
        {
            'appointment': inst_,
        }
    )


    msg = EmailMultiAlternatives(
        subject=f'Регистрацмя на сайте SAKHLIS-REMONTI.GE',  #TODO сделать нормальный шаблон...
        from_email='alp-rostov@mail.ru',
        to=[inst_.email],
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем



