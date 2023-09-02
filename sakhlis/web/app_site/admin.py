from django.contrib import admin
from .models import *

class OrderListAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_order', 'customer_name', 'customer_phone')
    list_display_links = ('text_order', 'customer_name', 'customer_phone')
    search_fields = ('text_order', 'customer_phone')
    list_filter = ('order_status', 'repairer_id')

admin.site.register(RepairerList)
admin.site.register(Service)
admin.site.register(Invoice)
admin.site.register(OrderList, OrderListAdmin)
