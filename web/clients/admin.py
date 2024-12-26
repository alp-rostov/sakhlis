from django.contrib import admin

from clients.models import UserProfile


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer_name', 'phone',
                    'telegram','whatsapp', 'city',
                    'profile', 'foto', 'user', 'qrcode_id')

admin.site.register(UserProfile,  ClientsAdmin)
