import telebot
from celery import shared_task
from .models import OrderList, RepairerList
from .utils import set_coordinates_address, add_telegram_button

TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
CHAT_ID = 5621399532


@shared_task
def send_order_information(inst):
    """" send information to repairman about order using telegram """
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
