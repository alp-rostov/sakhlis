from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.http import Http404
from clients.models import UserProfile
from .models import ApartmentPhoto, Apartment
from .form import ApartmentFormAddPhoto


class ApartmentPhotoUpdate(LoginRequiredMixin, UpdateView):
    model = ApartmentPhoto
    template_name = 'apartment/apartment_update_photo.html'
    form_class = ApartmentFormAddPhoto
    success_url = '/apartments'

    def get_object(self, queryset=None):
        apartment=Apartment.objects.filter(pk=self.kwargs['pk'])
        owner=apartment.first().owner
        user_auth=UserProfile.objects.get(user=self.request.user)
        if owner==user_auth or self.request.user.is_superuser:
            self.form_class.base_fields['id_apartments'].queryset = apartment
            try:
                return super().get_object(queryset)
            except Http404:
                return None
        else:
            raise Http404("")

    def get_success_url(self):
        dict_choice_url = {'repairer': '/list_order/'+self.request.GET.get('pk'), 'owner': '/client/'}
        return dict_choice_url[self.request.user.groups.first().name]
