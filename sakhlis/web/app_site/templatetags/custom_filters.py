from django import template
from ..models import CITY_CHOICES, AREA_CHOICES

register = template.Library()


@register.filter()
def city_tag(value):
    a = dict((i, j) for i, j in CITY_CHOICES)
    return f'{a[value]}'

@register.filter()
def area_tag(value):
    a = dict((i, j) for i, j in AREA_CHOICES)
    return f'{a[value]}'
