from django import template
from ..models import CITY_CHOICES, ORDER_STATUS, MONTH

register = template.Library()


@register.filter()
def choice_tag(value, A):
    try:
        if A == 'city':
            a = dict(CITY_CHOICES)
        elif A == 'status_order':
            a = dict(ORDER_STATUS)
        elif A == 'month':
            a = dict(MONTH)
        return f'{a[value]}'

    except KeyError:
        return f''


@register.filter()
def finish_order_tag(value):
    return f'' if value else f' в работе...'
