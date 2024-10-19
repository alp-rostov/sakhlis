from django import template
from app_site.constants import CITY_CHOICES, ORDER_STATUS_, MONTH, WORK_CHOICES

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary.get(key):
        return dictionary.get(key)
    else:
        return '-'

@register.filter()
def choice_tag(value, A):
    try:
        if A == 'city':
            a = dict(CITY_CHOICES)
        elif A == 'status_order':
            a = dict(ORDER_STATUS_)
        elif A == 'month':
            a = dict(MONTH)
        elif A == 'work_type':
            a = dict(WORK_CHOICES)
        return f'{a[value]}'

    except KeyError:
        return f''


@register.filter()
def finish_order_tag(value):
    return f'' if value else f' в работе...'


@register.filter()
def change_comma_to_dot(value):
    return str(value).replace(',', '.')
