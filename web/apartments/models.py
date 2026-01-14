from django.db import models
from pathlib import Path
import os
from web.settings_prod  import BASE_DIR
from app_site.constants import APART_CHOICES, CITY_CHOICES


class Apartment(models.Model):
    """Clients' apartments"""
    name = models.CharField(max_length=150, verbose_name='Name', null=True, blank=True, default='')
    type = models.CharField(max_length=2, choices=APART_CHOICES, default='FL', null=True, blank=True,
                            verbose_name='Type')
    owner = models.ForeignKey('clients.UserProfile', on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Responsible person for apartment')
    address_city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB', null=True, blank=True,
                                    verbose_name='City')
    address_street_app = models.CharField(max_length=150, verbose_name='Street', null=True, blank=True, default=' ')
    address_num = models.CharField(max_length=150, verbose_name='Apartment (number, entrance, floor etc.)', null=True, blank=True, default=' ')
    # foto = models.ImageField(upload_to="images/appartment/", null=True, blank=True, verbose_name='Photo:')
    link_location = models.CharField(max_length=300, null=True, blank=True, verbose_name='Link location', default='')

    class Meta:
        verbose_name = 'Appartment'
        verbose_name_plural = 'Appartments'

    def __str__(self):
        return f"{self.address_street_app} {self.address_num} "


class ApartmentPhoto(models.Model):
    """Clients' apartments"""
    id_apartments = models.OneToOneField('Apartment', on_delete=models.CASCADE , primary_key = True,
                              verbose_name='Id apartments')

    photo = models.ImageField(upload_to="images/appartment/", null=True, blank=True, verbose_name='Photo:')

    def save(self, *args, **kwargs):
        filename=self.photo.name=str(self.id_apartments.pk)+'.jpg'
        try:
            os.remove(os.path.join(BASE_DIR, 'media/images/appartment', filename))
        except FileNotFoundError:
            pass
        self.photo.name=str(self.id_apartments.pk)+'.jpg'
        super().save(*args, **kwargs)
        super().save()


    class Meta:
        verbose_name = 'Appartment_photo'
        verbose_name_plural = 'Appartments_photo'

# class StreetTbilisi(models.Model):
#     type_street = models.CharField(max_length=50)
#     name_street = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name = 'Street'
#         verbose_name_plural = 'Street'
#
#     def __str__(self):
#         return f'{self.name_street} {self.type_street}'
