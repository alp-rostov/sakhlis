from django.contrib import admin

from mails.models import Client


class MailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mail', 'flag')

admin.site.register(Client,  MailAdmin)
