from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Exists, Subquery, OuterRef, Count, Sum, F
from django.http import JsonResponse
from django.views.generic import ListView, UpdateView, TemplateView, DetailView, CreateView
from django.shortcuts import redirect, get_object_or_404

from apartments.models import Apartment
from app_site.constants import PERMISSION_FOR_REPAIER, PERMISSION_FOR_OWNER
from app_site.exeptions import BaseClassExeption
from app_site.filters import OrderFilter
from app_site.forms import ApartentUpdateForm
from app_site.models import OrderList, Invoice
from app_site.repository import DataFromRepairerList, DataFromInvoice
from app_site.views import OrderManagementSystem, OrderCreate
from clients.filters import ClientFilter
from clients.form import CustomerForm, CustomerFormForModal
from clients.models import UserProfile


class OwnerDetailInformation(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'owner/owner_profile.html'
    permission_required = PERMISSION_FOR_OWNER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prof'] = DataFromRepairerList().get_object_from_UserProfile(user=self.request.user)

        context['order_list_by_apartments'] = (
            OrderList.objects.only('time_in', 'text_order', 'apartment_id__address_street_app',
                                   'apartment_id__address_num', 'apartment_id__name',
                                   'apartment_id__address_city', 'apartment_id__foto', 'order_status',
                                   'repairer_id__username')
            .filter(customer_id=context['prof'])
            .order_by('apartment_id__address_street_app', '-time_in')
            .select_related('apartment_id', 'repairer_id')
        )
        #  apartments` list for top buttons
        context['apartments'] = (Apartment.objects
                                 .filter(owner=context['prof'])
                                 .annotate(top=Subquery(Exists(OrderList.objects.filter(apartment_id=OuterRef('pk')).exclude(order_status='END'))))
                                 .only('pk', 'address_city', 'address_street_app', 'address_num', 'foto',
                                        'name')
                                 .order_by('name', 'address_street_app'))
        # detail info of apartments wich have no orders
        list_app_ = set([i.get('apartment_id') for i in context['order_list_by_apartments'].values('apartment_id')])
        list_app = context['apartments'].exclude(pk__in=list_app_)
        context['list_app'] = list_app
        return context

class ApartmentOwner(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Apartment
    template_name = 'owner/apartment.html'
    permission_required = PERMISSION_FOR_OWNER
    context_object_name = 'appartment'

    def get_queryset(self):
        _=UserProfile.objects.get(user=self.request.user)
        return (Apartment.objects
                .filter(owner=_)
                .order_by('address_street_app'))

    def get_context_data(self, *, object_list=None, **kwargs):
        _=UserProfile.objects.get(user=self.request.user)  # TODO delete DRY
        context=super().get_context_data(**kwargs)

        list_orders_master=OrderList.objects.filter(apartment_id__owner=_)

        orders_quantity = list_orders_master.values('apartment_id').annotate(
            quantity=Count("apartment_id"))
        count = {}
        for i in orders_quantity:
            count[i['apartment_id']] = i['quantity']
        context['orders_count'] = count

        orders_amount = (Invoice.objects
             .filter(order_id__apartment_id__owner_id=_)
             .values('order_id__apartment_id')
             .annotate(ss=Sum(F('price')*F('quantity')))
             )
        summ = {}
        for ii in orders_amount:
            summ[ii['order_id__apartment_id']] = str(ii['ss'])
        context['orders_summ'] = summ

        masters={}
        list_masters = list_orders_master.exclude(repairer_id=None).values('apartment_id','repairer_id', 'repairer_id__username').distinct()
        for iii in list_masters:
            if not masters.get(iii.get('apartment_id')):
                masters[iii['apartment_id']] = [(iii['repairer_id'], iii['repairer_id__username'])]
            else:
                t= masters.get(iii.get('apartment_id'))
                t.append((iii['repairer_id'], iii['repairer_id__username']))
                masters[iii['apartment_id']]=t
        context['list_master'] = masters

        return context

class OwnerOrderManagementSystem(OrderManagementSystem, LoginRequiredMixin, ListView):
    """ list of all orders """
    template_name = 'owner/order_list.html'
    permission_required = PERMISSION_FOR_OWNER

    def get_queryset(self):
        userprof = UserProfile.objects.get(user=self.request.user)
        queryset = OrderList.objects \
            .filter(customer_id=userprof) \
            .select_related('apartment_id', 'repairer_id') \
            .values('pk', 'time_in',
                    'text_order', 'apartment_id','repairer_id',
                    'repairer_id__username', 'apartment_id__address_street_app',
                    'apartment_id__address_city', 'apartment_id__address_num', 'apartment_id__name'
                    ).order_by('-time_in')
        self.filterset = OrderFilter(self.request.GET, queryset)
        return self.filterset.qs


class OwnerInvoice(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """ list of all orders """
    model = OrderList
    context_object_name = 'info'
    template_name = 'owner/owner_invoice.html'
    permission_required = PERMISSION_FOR_OWNER

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['invoice'] = DataFromInvoice().get_data_from_invoice_with_amount(order_id_=self.object.pk)
        return context

class OwnerApartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Apartment
    template_name = 'owner/apartment_update.html'
    form_class = ApartentUpdateForm
    success_url = '../apartments'

class OwnerApartmentCreate(LoginRequiredMixin, CreateView):
    model = Apartment
    template_name = 'owner/apartment_update.html'
    form_class = ApartentUpdateForm
    success_url = '../apartment'

    def form_valid(self, form):
        super().form_valid(form)
        form.instance.owner = UserProfile.objects.get(user=self.request.user)
        form.save()
        return redirect('apartments')

class ClientsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """UPDATE INFORMATION ABOUT CLIENT"""
    model = UserProfile
    template_name = 'repairer/clients_update.html'
    form_class = CustomerForm
    permission_required = PERMISSION_FOR_REPAIER

    def get_success_url(self):
        if self.request.GET.get('pk'):
            dict_choice_url = {'repairer': '/list_order/' + self.request.GET.get('pk'), 'owner': '/owner/apartment'}
            return dict_choice_url[self.request.user.groups.first().name]
        else:
            return '../../clients'

# def clent_create_api(request):
#     _=request.POST.get('qr-code')[8:]
#     if request.method == 'POST' and UserProfile.objects.get(qrcode_id=_):
#         form = CustomerFormForModal(request.POST)
#         form.instance.save()
#     return JsonResponse({'message': ''})

