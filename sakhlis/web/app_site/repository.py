from django.contrib.auth.models import User
from django.db.models import Count, Sum, F

from app_site.models import *


class DataFromRepairerList:
    @staticmethod
    def get_object_from_RepairerList(user:User) ->RepairerList:
        return RepairerList.objects.get(user=user)

class DataFromOrderList:
    @staticmethod
    def get_number_of_orders_from_OrderList(repairer:User) -> int:
        return OrderList.objects\
            .values('repairer_id')\
            .annotate(count=Count('repairer_id'))\
            .filter(repairer_id=repairer)[0]['count']

    @staticmethod
    def get_data_from_OrderList_all(repairer: User):
        return OrderList.objects\
                .filter(repairer_id=repairer)\
                .order_by("-pk")
    @staticmethod
    def get_data_from_OrderList_with_order_status(repairer: User, status_of_order:str):
        return OrderList.objects \
                .filter(repairer_id=repairer, order_status=status_of_order) \
                .order_by("-pk")

    @staticmethod
    def get_next_number_for_paginator_from_OrderList(repairer: User, pk:int):
        return OrderList.objects.filter(pk__gt=pk, repairer_id=repairer).values('pk').first()
    @staticmethod
    def get_previous_number_for_paginator_from_OrderList(repairer: User, pk:int):
        return OrderList.objects.filter(pk__lt=pk, repairer_id=repairer).order_by('-pk').values('pk').first()

    @staticmethod
    def get_monthly_order_cost_from_OrderList(repairer: User):
        return OrderList.objects \
            .values('time_in__month', 'time_in__year') \
            .annotate(count=Sum(F('invoice__price') * F('invoice__quantity'))) \
            .filter(repairer_id=repairer) \
            .order_by('time_in__year')

    @staticmethod
    def get_monthly_order_quantity_from_OrderList(repairer: User):
        return OrderList.objects\
            .values('time_in__month', 'time_in__year')\
            .annotate(count=Count(F('pk')))\
            .filter(repairer_id=repairer)\
            .order_by('time_in__year')

    def get_dayly_cost_of_orders(repairer: User):
        return OrderList.objects \
                   .values('time_in__date') \
                   .annotate(count=Sum(F('invoice__price') * F('invoice__quantity'))) \
                   .order_by('-time_in__date') \
                   .filter(repairer_id=repairer)[0:30:-1]

class DataFromInvoice:
    @staticmethod
    def get_amount_money_of_orders(repairer:User) -> float:
        return Invoice.objects\
            .values('order_id__repairer_id')\
            .annotate(sum=Sum(F('price') * F('quantity')))\
            .filter(order_id__repairer_id=repairer)[0]['sum']

    @staticmethod
    def get_data_from_Invoice_with_amount(order_id_: int):
        return Invoice.objects \
        .filter(order_id=order_id_) \
        .select_related('service_id') \
        .defer('service_id__type') \
        .annotate(amount=F('price') * F('quantity'))


    @staticmethod
    def get_quantity_of_orders_by_type(repairer: User):
        return Invoice.objects \
            .values('service_id__type') \
            .annotate(count=Count(F('service_id__type'))) \
            .order_by('-count') \
            .filter(order_id__repairer_id=repairer)


    @staticmethod
    def get_cost_of_orders_by_type(repairer: User):
        return Invoice.objects \
            .values('service_id__type') \
            .annotate(count=Sum(F('price') * F('quantity'))) \
            .order_by('-count') \
            .filter(order_id__repairer_id=repairer)


