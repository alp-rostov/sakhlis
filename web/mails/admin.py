from django.contrib import admin

from mails.models import Client


class MailAdmin(admin.ModelAdmin):
    list_display = ('mail','flaf')
    list_display_links = ('pk', 'customer_name',)

admin.site.register(Client, MailAdmin)

# Register your models here.
