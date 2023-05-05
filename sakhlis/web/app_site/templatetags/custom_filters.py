from django import template
from ..models import CITY_CHOICES, AREA_CHOICES

register = template.Library()


@register.filter()
def choice_tag(value, A):
    try:
        a = dict(CITY_CHOICES) if A=='city' else dict(AREA_CHOICES)
        return f'{a[value]}'
    except KeyError:
        return f''
