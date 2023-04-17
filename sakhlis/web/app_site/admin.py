from django.contrib import admin
from .models import CityDirectory, RepairerList, OrderList

admin.site.register(CityDirectory)
admin.site.register(RepairerList)
admin.site.register(OrderList)

# Register your models here.
