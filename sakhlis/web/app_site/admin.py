from django.contrib import admin
from .models import RepairerList, OrderList, Invoice, Service

admin.site.register(RepairerList)
admin.site.register(Service)
admin.site.register(Invoice)

@admin.register(OrderList)
class TestAdmin(admin.ModelAdmin):
    readonly_fields = ['time_in']
