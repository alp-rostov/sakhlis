from django.contrib import admin

from mails.models import Mail


class MailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mail', 'flag')

admin.site.register(Mail,  MailAdmin)
