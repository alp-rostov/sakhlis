from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, UpdateView

from app_site.constants import PERMISSION_FOR_REPAIER
from clients.filters import ClientFilter
from clients.form import CustomerForm
from clients.models import UserProfile


class Clients(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = 'clients'
    template_name = 'repairer/clients.html'
    permission_required = PERMISSION_FOR_REPAIER
    queryset = UserProfile.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('customer_name') is not None:
            queryset = UserProfile.objects.order_by('customer_name').all()
            # queryset = DataFromUserProfile().get_clients_of_orders_from_UserProfile(self.request.user)
        self.filterset = ClientFilter(self.request.GET, queryset)
        return self.filterset.qs


class ClientsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'repairer/clients_update.html'
    form_class = CustomerForm
    permission_required = PERMISSION_FOR_REPAIER

    def get_success_url(self):
        dict_choice_url = {'repairer': '/list_order/'+self.request.GET.get('pk'), 'owner': '/owner/apartment'}
        return dict_choice_url[self.request.user.groups.first().name]
