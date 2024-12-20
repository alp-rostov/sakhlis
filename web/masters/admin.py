from django.contrib import admin

from masters.models import MasterProfile


class MasterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'phone', 'telegram',
                    'whatsapp','city','profile')

admin.site.register(MasterProfile,  MasterAdmin)
