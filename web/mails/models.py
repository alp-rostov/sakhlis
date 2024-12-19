from django.db import models

class Client(models.Model):
    """list of clients` mails for sending offers"""
    mail = models.EmailField(null=True, blank=True)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mail}"
