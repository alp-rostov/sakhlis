from django.contrib import admin

from .models import *


class PersonalInvoice(admin.TabularInline):
    model = Invoice


class OrderListAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_in', 'apartment_id', 'text_order',
                    'customer_id', 'repairer_id',  'apartment_id')
    list_display_links = ('id', )
    list_filter = ('repairer_id', 'customer_id')
    inlines = [PersonalInvoice]

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'order_id', 'quantity', 'price')
    list_display_links = ('service_id', 'order_id', 'quantity', 'price')
    list_filter = ('service_id', )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'type')
    list_display_links = ('pk', 'name', 'type')
    list_filter = ('type', )

admin.site.register(Service, ServiceAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(OrderList, OrderListAdmin)
