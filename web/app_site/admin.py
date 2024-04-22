from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import *

class PersonalInvoice(admin.TabularInline):
    model = Invoice

class OrderListAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_in', 'time_out', 'text_order')
    list_display_links = ('text_order', )
    search_fields = ('text_order', )
    list_filter = ('order_status', 'repairer_id', 'time_in')
    inlines = [PersonalInvoice]

class FeedbackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_feedback', 'mark')
    list_display_links = ('id', )



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

class AppartamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address_city',
                    'address_street_app','address_num', 'foto',
                    'location_longitude','location_latitude', 'notes')
    list_display_links = ('name',)



admin.site.register(UserProfile)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(StreetTbilisi, StreetAdmin)
admin.site.register(Apartment, AppartamentAdmin)
admin.site.register(ClientFeedback, FeedbackListAdmin)
