import telebot
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import OrderList

import telebot



@receiver(post_save, sender=OrderList)
def send_post_new_order(instance, created, **kwargs):
    if created:
        html_content = render_to_string(
        'email.html',
        {
        'instance': instance,
        }
        )
        subject_=f'Заказ на работы № {instance.pk} от {instance.time_in.strftime("%Y-%M-%d")}'
        from_= 'alp-rostov@mail.ru'
        text =subject_ + f'\n ИМЯ: {instance.customer_name } \n ТЕЛЕФОН: {instance.customer_phone } \n ' \
                         f'АДРЕС: {instance.address_street_app} \n ОПИСАНИЕ ПРОБЛЕМЫ:{instance.text_order} '
        msg = EmailMultiAlternatives(
            subject=subject_,
            body='',  # это то же, что и message
            from_email=from_,
            to=['alprostov.1982@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

        TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
        bot = telebot.TeleBot(TOKEN)
        chat_id = 5621399532
        bot.send_message(chat_id, text)




