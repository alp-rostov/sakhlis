from django.contrib import admin
from .models import *

class PersonalInvoice(admin.TabularInline):
    model = Invoice

class OrderListAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_in', 'text_order', 'customer_name', 'customer_phone', 'location_longitude', 'location_latitude')
    list_display_links = ('text_order', 'customer_name', 'customer_phone')
    search_fields = ('text_order', 'customer_phone')
    list_filter = ('order_status', 'repairer_id', 'time_in')
    inlines = [PersonalInvoice]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'order_id', 'quantity', 'price')
    list_display_links = ('service_id', 'order_id', 'quantity', 'price')
    list_filter = ('service_id', )

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_display_links = ('name', 'type')
    list_filter = ('type', )


class StreetAdmin(admin.ModelAdmin):
    list_display = ('type_street', 'name_street')
    list_display_links = ('type_street', 'name_street')



admin.site.register(Repairer)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(StreerTbilisi, StreetAdmin)
