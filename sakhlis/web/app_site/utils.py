from geopy.geocoders import Nominatim
from telebot import types


def set_coordinates_address(street: str, city: str) -> str:
    """ setting of coordinates by street and city """
    try:
        geolocator = Nominatim(user_agent="app_site", )
        location = geolocator.geocode({'street': {street}, 'city': {city}}, addressdetails=True)
    except TypeError:
        return ' '
    else:
        if location:
            return f'https://yandex.ru/maps/?pt={location.longitude},{location.latitude}&z=18&l=map'
        else:
            return ' '


def add_telegram_button(repairer: list, order_pk: int):
    """
    creating buttons for telegram message.
    repairer -> list of tuples (id repairer, s_name repairer)
    order_pk -> order`s number
    """
    # создание кнопок в телеграмм
    keyboard = types.InlineKeyboardMarkup()
    button = []
    for i in repairer:
        url_ = f'http://127.0.0.1:8000/add?pk_order=' \
               f'{order_pk}&pk_repairer={i[0]}'
        button.append(types.InlineKeyboardButton(text=i[1], url=url_))
    return keyboard.add(*button)
