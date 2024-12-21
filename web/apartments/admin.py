from django.contrib import admin

from apartments.models import Apartment


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('address_city', 'address_street_app', 'address_num',
                    'name', 'type', 'owner', 'foto', 'notes' )

admin.site.register(Apartment, ApartmentAdmin)
