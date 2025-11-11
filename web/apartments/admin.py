from django.contrib import admin

from apartments.models import Apartment, ApartmentPhoto


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('address_city', 'address_street_app', 'address_num',
                    'name', 'type', 'owner', 'foto')

class ApartmentPhotoAdmin(admin.ModelAdmin):
    list_display = ('id_apartments', 'photo')


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentPhoto, ApartmentPhotoAdmin)
