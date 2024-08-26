from django.db.models import Count, Sum, F, Prefetch, QuerySet
from app_site.models import *

class DataFromRepairerList:
    model = UserProfile.objects

    def get_object_from_UserProfile(self, user: User) -> UserProfile:
        return self.model.get(user=user)


class DataFromUserProfile:

    def __init__(self, model=UserProfile.objects):
        self.model = model

    def get_clients_of_orders_from_UserProfile(self,
                                               user: User) -> QuerySet:  # TODO refactor queryset 'customer_id__gt=0'
        list_orders = OrderList.objects \
            .values('customer_id') \
            .filter(customer_id__gt=0) \
            # .annotate(count=Count(F('pk')))
        return (self.model
                .filter(pk__in=list_orders)
                .values('pk', 'customer_name', 'profile', 'foto')
                .order_by('customer_name'))


class DataFromOrderList:

    def __init__(self, model=OrderList.objects):
        self.model = model

    def get_number_of_orders_from_orderList(self, repairer: User) -> int:
        return self.model \
            .values('repairer_id') \
            .annotate(count=Count('repairer_id')) \
            .filter(repairer_id=repairer)[0]['count']

    def get_data_from_orderList_all(self, repairer: User) -> QuerySet:
        return self.model \
            .filter(repairer_id=repairer) \
            .select_related('apartment_id', 'customer_id') \
            .order_by("-pk")

    def get_data_from_OrderList_with_order_status(self, status_of_order: list, repairer: User = 'None') -> QuerySet:
        if repairer:
            return self.model \
                .exclude(order_status='END') \
                .select_related('apartment_id', 'customer_id', 'repairer_id') \
                .order_by("order_status", "-pk")
        else:
            return self.model \
                .exclude(order_status='END') \
                .select_related('apartment_id', 'customer_id', 'repairer_id') \
                .order_by("order_status", "-pk")

    def get_next_number_for_paginator_from_OrderList(self, pk: int,             # TODO refactor repeatable code
                                                     repairer: User = None) -> OrderList:
        if repairer:
            return self.model \
                .filter(pk__gt=pk, repairer_id=repairer) \
                .values('pk') \
                .first()
        else:
            return self.model \
                .filter(pk__gt=pk) \
                .values('pk') \
                .first()

    def get_previous_number_for_paginator_from_OrderList(self, pk: int,         # TODO refactor repeatable code
                                                         repairer: User = None) -> OrderList:
        if repairer:
            return self.model \
                .filter(pk__lt=pk, repairer_id=repairer) \
                .order_by('-pk') \
                .values('pk') \
                .first()
        else:
            return self.model \
                .filter(pk__lt=pk) \
                .order_by('-pk') \
                .values('pk') \
                .first()

    def get_monthly_order_cost_from_OrderList(self, repairer: User) -> QuerySet:
        return self.model \
            .values('time_in__month', 'time_in__year') \
            .annotate(count=Sum(F('invoice__price') * F('invoice__quantity'))) \
            .order_by('time_in__year', 'time_in__month').all()

    def get_monthly_order_quantity_from_OrderList(self, repairer: User) -> QuerySet:
        return self.model \
            .values('time_in__month', 'time_in__year') \
            .annotate(count=Count(F('pk'))) \
            .order_by('time_in__year').all()

    def get_dayly_cost_of_orders(self, repairer: User) -> QuerySet:
        return self.model \
                   .values('time_in__date') \
                   .annotate(count=Sum(F('invoice__price') * F('invoice__quantity'))) \
                   .order_by('-time_in__date').all()[0:30:-1]

    def get_all_data_of_order_with_from_invoice(self):
        return self.model \
            .prefetch_related(Prefetch('invoice_set', Invoice.objects
                                       .defer('quantity_type', 'service_id__type')
                                       .select_related('service_id')
                                       .annotate(sum=F('price') * F('quantity')))
                              ) \
            .select_related('repairer_id')


class DataFromInvoice:
    def __init__(self, model=Invoice.objects):
        self.model = model

    def get_amount_money_of_orders(self, repairer: User) -> float:
        return self.model \
            .values('order_id__repairer_i0d') \
            .annotate(sum=Sum(F('price') * F('quantity'))) \
            .filter(order_id__repairer_id=repairer)[0]['sum']

    def get_data_from_invoice_with_amount(self, order_id_: int):
        return self.model \
            .filter(order_id=order_id_) \
            .select_related('service_id') \
            .defer('service_id__type') \
            .annotate(amount=F('price') * F('quantity'))

    def get_quantity_of_orders_by_type(self, repairer: User):
        return self.model \
            .values('service_id__type') \
            .annotate(count=Count(F('service_id__type'))) \
            .order_by('-count').all() \

    def get_cost_of_orders_by_type(self, repairer: User):
        return self.model \
            .values('service_id__type') \
            .annotate(count=Sum(F('price') * F('quantity'))) \
            .order_by('-count').all() \

    def get_total_cost_of_some_orders(self, list_of_orders: QuerySet) -> QuerySet:
        return self.model \
            .filter(order_id__in=list_of_orders) \
            .aggregate(Summ=Sum(F('price') * F('quantity'))).get('Summ')
