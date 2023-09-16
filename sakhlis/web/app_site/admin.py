from django.contrib import admin
from .models import *

class OrderListAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_in', 'text_order', 'customer_name', 'customer_phone')
    list_display_links = ('text_order', 'customer_name', 'customer_phone')
    search_fields = ('text_order', 'customer_phone')
    list_filter = ('order_status', 'repairer_id', 'time_in')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'order_id', 'quantity', 'price')
    list_display_links = ('service_id', 'order_id', 'quantity', 'price')
    list_filter = ('service_id', )

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_display_links = ('name', 'type')
    list_filter = ('type', )

admin.site.register(RepairerList)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(OrderList, OrderListAdmin)
