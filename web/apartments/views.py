from decimal import getcontext

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


from app_site.constants import *


from .models import ApartmentPhoto, Apartment
from .form import ApartmentFormAddPhoto


class ApartmentPhotoUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = ApartmentPhoto
    template_name = 'apartment/apartment_update_photo.html'
    form_class = ApartmentFormAddPhoto
    permission_required = PERMISSION_FOR_REPAIER
    success_url = '/apartments'

    def get_object(self, queryset=None):
        self.form_class.base_fields['id_apartments'].queryset = Apartment.objects.filter(pk=self.kwargs['pk'])
        try:
            return super().get_object(queryset)
        except Http404:
            return None
