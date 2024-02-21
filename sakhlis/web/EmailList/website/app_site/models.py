# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Email(models.Model):
    """l_name, s_name, birthday, email """
    l_name = models.\
        CharField(null=True, blank=True, max_length=50, verbose_name='Имя')
    s_name = models.\
        CharField(null=True, blank=True, max_length=50, verbose_name='Фамилия')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    email = models.EmailField(null=True, blank=True, verbose_name='Почта')

    def __str__(self):
        return self.email