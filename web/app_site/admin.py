from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import *


class PersonalInvoice(admin.TabularInline):
    model = Invoice


class PersonalApartment(admin.TabularInline):
    model = Apartment


class PersonalOrders(admin.TabularInline):
    model = OrderList


class OrderListAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_in', 'repairer_id', 'apartment_id', 'text_order',
                    'customer_id', 'repairer_id',  'apartment_id')
    list_display_links = ('id', )
    list_filter = ('repairer_id', 'customer_id')
    inlines = [PersonalInvoice]


class FeedbackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_feedback', 'mark')
    list_display_links = ('id', )


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'order_id', 'quantity', 'price')
    list_display_links = ('service_id', 'order_id', 'quantity', 'price')
    list_filter = ('service_id', )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'type')
    list_display_links = ('pk', 'name', 'type')
    list_filter = ('type', )


class StreetAdmin(admin.ModelAdmin):
    list_display = ('type_street', 'name_street')
    list_display_links = ('type_street', 'name_street')


class AppartamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'owner', 'address_city',
                    'address_street_app','address_num', 'foto',
                    'notes')
    list_display_links = ('pk', 'name',)
    list_filter = ('owner',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer_name', 'phone', 'telegram', 'whatsapp',
                    'profile', 'user')
    list_display_links = ('pk', 'customer_name',)
    list_filter = ('telegram',)
    search_fields = ('telegram',)
    inlines = [PersonalOrders]



admin.site.register(UserProfile, UserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(StreetTbilisi, StreetAdmin)
admin.site.register(Apartment, AppartamentAdmin)
admin.site.register(ClientFeedback, FeedbackListAdmin)
