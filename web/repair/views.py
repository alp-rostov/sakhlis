from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView

from app_site.constants import PERMISSION_FOR_REPAIER


class RepairerDetailInformation(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'repairer/repaier_profile.html'
    permission_required = PERMISSION_FOR_REPAIER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_order'] = OrderForm
        context['form_appart'] = ApartmentForm
        context['form_customer'] = CustomerForm               # TODO refactor filter 3 is a group`s number 'repaier'
        context['list_masters'] = User.objects.filter(groups=3).values('pk', 'username', 'groups')
        context['orders'] = DataFromOrderList().get_data_from_OrderList_with_order_status(repairer=self.request.user,
                                                                                          status_of_order=['SND',
                                                                                                           'RCV'])
        return context


class RepaierUpdate(BaseClassExeption, PermissionRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'repairer/repaier_create.html'
    form_class = CustomerForm
    permission_required = PERMISSION_FOR_REPAIER

    def get_success_url(self):
        return '/user/' + str(self.request.user.pk)
