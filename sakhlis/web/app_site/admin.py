from django.contrib import admin
from .models import RepairerList, OrderList

admin.site.register(RepairerList)


@admin.register(OrderList)
class TestAdmin(admin.ModelAdmin):
    readonly_fields = ['time_in']
