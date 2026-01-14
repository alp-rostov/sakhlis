from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.http import Http404
from clients.models import UserProfile
from .models import ApartmentPhoto, Apartment
from .form import ApartmentFormAddPhoto, ApartmentFormUpdate

def dict_choice_url(pk, usergroup):  #TODO refactor this
    if pk is None:
        pk=' '
    choice_url = {'repairer': '/list_order/' + pk, 'owner': '/client/'}
    if pk=='0':
        choice_url['repairer'] ='/user/51'
    return choice_url[usergroup]


class ApartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Apartment
    template_name = 'apartment/apartment_update.html'
    form_class = ApartmentFormUpdate

    def get_object(self, queryset=None):
        apartment=Apartment.objects.filter(pk=self.kwargs['pk'])
        owner=apartment.first().owner
        user_auth=UserProfile.objects.get(user=self.request.user)
        self.form_class.base_fields['id_apartments'].queryset = apartment
        if owner==user_auth or self.request.user.is_superuser:
            try:
                return super().get_object(queryset)
            except Http404:
                return None
        else:
            raise Http404("")

    def get_success_url(self):
        return dict_choice_url(self.request.GET.get('pk'), self.request.user.groups.first().name)

class ApartmentPhotoUpdate(ApartmentUpdate):
    model = ApartmentPhoto
    template_name = 'apartment/apartment_update_photo.html'
    form_class = ApartmentFormAddPhoto

