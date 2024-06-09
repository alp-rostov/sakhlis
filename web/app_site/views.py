import json
import logging
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView

from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .constants import *
from .exeptions import BaseClassExeption
from .filters import OrderFilter, ClientFilter
from .models import *
from .forms import *
from .repository import DataFromRepairerList, DataFromOrderList, DataFromInvoice, DataFromUserProfile
from .utils import *

logger = logging.getLogger(__name__)


class ApartmentList(ListView):
    model = Apartment
    context_object_name = 'appartment'
    template_name = 'owner/apartment.html'

    def get_queryset(self):
        userptofile=UserProfile.objects.get(user=self.request.user)
        return Apartment.objects.filter(owner=userptofile)


class Clients(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, ListView):
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
        if self.request.GET.get('customer_name')!=None:
            queryset = DataFromUserProfile().get_clients_of_orders_from_UserProfile(self.request.user)

        self.filterset = ClientFilter(self.request.GET, queryset)

        return self.filterset.qs


class ClientsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'repairer/clients_update.html'
    form_class = CustomerForm
    permission_required = PERMISSION_FOR_REPAIER
    def form_valid(self, form):
        if OrderList.objects.filter(customer_id=self.object, repairer_id=self.request.user).exists() and not self.object.user:
            form.save()
            url = reverse('user', args=(self.request.user.pk, ))
            return redirect(url)
        else:
            return redirect('error404')

class Error404(TemplateView):
    template_name = '404.html'


class InvoiceCreate(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """ Add name of works, quantity, price to order  """
    model = OrderList
    context_object_name = 'info'
    template_name = 'repairer/invoice.html'
    permission_required = PERMISSION_FOR_REPAIER

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['invoice'] = DataFromInvoice().get_data_from_Invoice_with_amount(order_id_=self.object.pk)
        context['type_work'] = WORK_CHOICES
        context['next'] = DataFromOrderList() \
            .get_next_number_for_paginator_from_OrderList(repairer=self.request.user, pk=self.object.pk)
        context['prev'] = DataFromOrderList() \
            .get_previous_number_for_paginator_from_OrderList(repairer=self.request.user, pk=self.object.pk)
        InvoiceFormSet = modelformset_factory(Invoice, form=InvoiceForm, extra=0)
        formset = InvoiceFormSet(queryset=Invoice.objects.none())
        context['form'] = formset
        return context

    def get_queryset(self):
        return DataFromOrderList().get_data_from_OrderList_all(repairer=self.request.user)

    def post(self, formset, **kwargs):
        b = get_object_or_404(OrderList, pk=self.kwargs.get('pk'))
        AuthorFormSet = modelformset_factory(Invoice, form=InvoiceForm)
        formset = AuthorFormSet(self.request.POST)
        try:
            instances = formset.save(commit=False)
        except ValueError:
            return JsonResponse('error', safe=False)

        list_num = []
        if instances:
            for instance in instances:
                instance.order_id = b
                instance.save()
                list_num.append({"pk": instance.pk,
                                 "quantity": instance.quantity,
                                 "price": instance.price,
                                 "service_id": instance.service_id.pk,
                                 "service_id_name": instance.service_id.name
                                 })

            return JsonResponse(list_num, safe=False)
        else:
            return JsonResponse({}, safe=False)


class OrderCreate(BaseClassExeption, CreateView):
    """" Add order """
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_appart'] = ApartmentForm
        context['form_customer'] = CustomerForm
        return context

    def form_valid(self, form):
        # if OrderCustomerForm(self.request.POST).is_valid() and ApartmentForm(self.request.POST).is_valid():
            with transaction.atomic():

                if self.request.user.is_authenticated and self.request.user.groups.first().name == 'owner':  # TODO add logic for owner and set a responseble person
                    form.instance.customer_id = UserProfile.objects.get(pk=self.request.POST.get('customer_id'))
                    form.instance.apartment_id = Apartment.objects.get(pk=self.request.POST.get('apartment_id'))
                    form.instance.order_status = 'SND'
                    form.instance.repairer_id = User.objects.get(pk=51)
                    form.save()
                    return JsonResponse({'message': f'<h3>Заявка № {form.instance.pk} отправлена успешно!</h3>',
                                         'pk': form.instance.pk,
                                         'text': form.instance.text_order,
                                         'date': form.instance.time_in,
                                         'repaier': form.instance.repairer_id.username,
                                         'apartment':form.instance.apartment_id.pk
                                         })

                elif self.request.user.is_authenticated and self.request.user.groups.first().name == 'repairer':
                    customer = OrderCustomerForm(self.request.POST).save()
                    app = ApartmentForm(self.request.POST).save(commit=False)
                    app.owner = customer
                    app.save()
                    form.instance.apartment_id = app
                    form.instance.customer_id = customer
                    form.instance.repairer_id = self.request.user
                    form.instance.order_status = 'SND'
                else:
                    customer = OrderCustomerForm(self.request.POST).save()
                    app = ApartmentForm(self.request.POST).save(commit=False)
                    app.owner = customer
                    app.save()
                    form.instance.apartment_id = app
                    form.instance.customer_id = customer
                    form.instance.order_status = 'BEG'

                form.save()
                return JsonResponse({'message': f'<h3>Заявка № {form.instance.pk} отправлена успешно!</h3>',
                                     'pk': form.instance.pk,
                                     'auth': self.request.user.is_authenticated
                                     })
        # else:
        #     return JsonResponse({'message': f'<h3>Ошибка, форма не валидна</h3>',
        #                          'pk': form.instance.pk,
        #                          'auth': self.request.user.is_authenticated
        #                          })


class OrderCreatebyRepaier(BaseClassExeption, CreateView):
    """" Add order """
    model = OrderList
    template_name = 'repairer/order_create_repairer.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class OrderDelete(BaseClassExeption, LoginRequiredMixin, DeleteView):
    model = OrderList
    template_name = 'order_delete.html'

    def get_success_url(self):
        if self.request.user.groups.first().name == 'owner':
            return f'/owner'
        elif self.request.user.groups.first().name == 'repairer':
            return '/list_order'


class OwnerDetailInformation(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'owner/owner_profile.html'
    permission_required = PERMISSION_FOR_OWNER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prof'] = DataFromRepairerList().get_object_from_UserProfile(user=self.request.user)
        context['order_list_by_apartments']=(OrderList.objects.only('time_in', 'text_order', 'apartment_id__address_street_app',
                                                       'apartment_id__address_num', 'apartment_id__name', 'apartment_id__notes',
                                                       'apartment_id__address_city', 'apartment_id__foto', 'order_status',
                                                       'repairer_id__username')
                                .filter(customer_id=context['prof'])
                                .order_by('apartment_id__address_street_app', '-time_in')
                                .select_related('apartment_id', 'repairer_id')
                                )

        context['apartments']=(Apartment.objects
                               .filter(owner=context['prof'])
                               .only('pk', 'address_city', 'address_street_app', 'address_num', 'foto', 'notes', 'name')
                               .order_by('address_street_app'))

        list_app_=set([i.get('apartment_id') for i in context['order_list_by_apartments'].values('apartment_id')])
        list_app=context['apartments'].exclude(pk__in=list_app_)
        context['list_app']=list_app
        return context


class OwnerInvoice(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """ list of all orders """
    model = OrderList
    context_object_name = 'info'
    template_name = 'owner/owner_invoice.html'
    permission_required = PERMISSION_FOR_OWNER
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['invoice'] = DataFromInvoice().get_data_from_Invoice_with_amount(order_id_=self.object.pk)
        return context


class OrderManagementSystem(BaseClassExeption, LoginRequiredMixin, ListView):
    """ list of all orders """
    model = OrderList
    context_object_name = 'order'
    template_name = 'repairer/order_list.html'
    permission_required = PERMISSION_FOR_REPAIER
    ordering = ['-time_in']

    def get_queryset(self):
        queryset = (super().get_queryset()
                    .filter(repairer_id=self.request.user)
                    .select_related('customer_id', 'apartment_id')
                    .values('pk', 'time_in',
                            'text_order', 'customer_id__pk',
                            'customer_id__customer_name','customer_id__phone',
                            'customer_id__telegram', 'customer_id__whatsapp',
                            'apartment_id__link_location', 'apartment_id__address_street_app',
                            'apartment_id__address_city', 'apartment_id__address_num'
                            ))
        self.filterset = OrderFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        c = context['filterset'].qs.values('pk')
        c_ = DataFromInvoice().get_total_cost_of_some_orders(list_of_orders=c)
        context['summ_orders'] = c_
        context['count_orders'] = self.get_queryset().count()
        return context


class OwnerOrderManagementSystem(OrderManagementSystem, BaseClassExeption, LoginRequiredMixin, ListView):
    """ list of all orders """
    template_name = 'owner/order_list.html'
    permission_required = PERMISSION_FOR_OWNER

    def get_queryset(self):
        userprof=UserProfile.objects.get(user=self.request.user)
        queryset = OrderList.objects \
                    .filter(customer_id=userprof) \
                    .select_related('apartment_id', 'repairer_id') \
                    .values('pk', 'time_in',
                            'text_order', 'apartment_id',
                            'repairer_id__username', 'apartment_id__address_street_app',
                            'apartment_id__address_city', 'apartment_id__address_num'
                            ).order_by('-time_in')
        self.filterset = OrderFilter(self.request.GET, queryset)
        return self.filterset.qs


class OwnerApartmentCreate(BaseClassExeption, LoginRequiredMixin, CreateView):
    model = Apartment
    template_name = 'owner/apartment_update.html'
    form_class = ApartentUpdateForm
    success_url = '../'

    def form_valid(self, form):
        form.instance.owner=UserProfile.objects.get(user=self.request.user)
        form.save()
        url = reverse('owner')
        return redirect(url)

class OwnerApartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Apartment
    template_name = 'owner/apartment_update.html'
    form_class = ApartentUpdateForm
    success_url = '../'


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderUpdateForm

    def get_form(self, **kwargs):
        form =OrderUpdateForm(self.request.user, **kwargs)
        return form
        # return self.form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_in'] = self.object.time_in
        context['pk'] = self.object.pk
        return context


    def get_success_url(self):
        return '/list_order/' + str(self.object.pk)


class RepairerDetailInformation(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'repairer/repaier_profile.html'
    # form_class = UserRegisterForm
    context_object_name = 'user'
    permission_required = PERMISSION_FOR_REPAIER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = DataFromRepairerList().get_object_from_UserProfile(user=self.object)
        context['count'] = DataFromOrderList().get_number_of_orders_from_OrderList(repairer=self.request.user)
        context['sum'] = DataFromInvoice().get_amount_money_of_orders(repairer=self.request.user)
        context['form_order'] = OrderForm
        context['form_appart'] = ApartmentForm
        context['form_customer'] = CustomerForm
        context['feedbacks'] = ClientFeedback.objects.all()
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


class Statistica(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'repairer/statistica.html'
    model = OrderList
    context_object_name = 'order'
    ordering = ['-time_in']
    permission_required = PERMISSION_FOR_REPAIER

    def get_queryset(self):
        queryset = super().get_queryset()
        # b = self.request.GET.copy()
        # b.__setitem__('repairer_id', self.request.user.pk)
        # self.filterset = OrderFilter(b, queryset)
        queryset = super().get_queryset().filter(repairer_id=self.request.user).select_related('customer_id',
                                                                                               'apartment_id').all()
        self.filterset = OrderFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filterset'] = self.filterset

        queryset_from_OrderList = self.filterset.qs

        list_objects_from_OrderList = list(queryset_from_OrderList)

        data_from_invoice = DataFromInvoice(Invoice.objects.filter(order_id__in=list_objects_from_OrderList))
        data_from_oder = DataFromOrderList(queryset_from_OrderList)

        context['form'] = OrderForm

        context['d'] = Graph(data_from_invoice.get_quantity_of_orders_by_type(repairer=self.request.user),
                             'service_id__type', 'count', WORK_CHOICES_, 'Order structure, quantity.', '') \
            .make_graf_pie()

        context['d_'] = Graph(data_from_invoice.get_cost_of_orders_by_type(repairer=self.request.user),
                              'service_id__type', 'count', WORK_CHOICES_, 'Order structure, lar.', '') \
            .make_graf_pie()

        context['f'] = Graph(data_from_oder.get_monthly_order_cost_from_OrderList(repairer=self.request.user),
                             'time_in__month', 'count', MONTH_, 'Earnings', 'lar') \
            .make_graf_bar()

        context['g'] = Graph(data_from_oder.get_monthly_order_quantity_from_OrderList(repairer=self.request.user),
                             'time_in__month', 'count', MONTH_, 'Order`s quantity', 'quantity') \
            .make_graf_bar()

        context['hh'] = Graph(data_from_oder.get_dayly_cost_of_orders(repairer=self.request.user),
                              'time_in__date', 'count', None, 'Dynamics', '') \
            .make_graf_plot()
        return context


class UserAuthorizationView(LoginView):
    def get_success_url(self):
        super().get_success_url()
        if 'repairer' == str(self.request.user.groups.first()):
            return reverse_lazy('user', kwargs={'pk': self.request.user.pk})
        elif 'owner' == str(self.request.user.groups.first()):
            return reverse_lazy('owner')


class UserRegisterView(CreateView):
    """ Registration of repairer """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'account/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = CustomerForm
        return context
    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save()
                group_ = self.request.POST.get('group')
                my_group = Group.objects.get(name=group_)
                my_group.user_set.add(self.object)
                profile=CustomerForm(self.request.POST, self.request.FILES).save(commit=False)
                profile.user=self.object
                profile.save()
                return redirect('home')
        except Exception as e:
            return redirect('../404.html')





def CreateIvoicePDF(request, **kwargs):
    """ Create invoice pdf-file for printing """

    # get information from models
    order_pk = kwargs.get("order_pk")
    info = DataFromOrderList().get_all_data_of_order_with_from_invoice().get(pk=order_pk)
    # create file
    buf = io.BytesIO()
    doc = InvoiceMaker(buf, info)
    doc.createDocument()
    doc.savePDF()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'Invoice_{order_pk}_.pdf')

@login_required
def OrderAddRepaier(request):
    """Add the repairer to order using telegram-bot"""
    order = get_object_or_404(OrderList, pk=request.GET['pk_order'])
    repaier = get_object_or_404(User, pk=request.GET['pk_repairer'])
    if order and repaier:
        if not order.repairer_id:
            order.repairer_id = repaier
            order.order_status = 'SND'
            order.save()
            return HttpResponseRedirect(reverse('update', args=(order.pk,)))
        else:
            return redirect('home')  # TODO настроить сообщение, что ремонтник уже указан

@login_required
def AddApartment(request):
    """Add"""
    if 'owner' == str(request.user.groups.first()):
        ApartmentForm(request.GET).save()
        print('---------------')

        #
        # return reverse_lazy('owner', kwargs={'pk': request.user.pk})
        #
        #
        #     return HttpResponseRedirect(reverse('update', args=(order.pk,)))
        # else:
        #     return redirect('home')


@login_required
def listservices_for_invoice_json(request, **kwargs):
    """for ajax request """
    data = Service.objects.filter(type=request.GET.get('type_work')).values('id', 'name')
    json_data = json.dumps(list(data))
    return JsonResponse(json_data, safe=False)

@login_required
def client_details_json(request, **kwargs):
    """for ajax request """
    data = UserProfile.objects.get(pk=request.GET.get('pk'))
    orders = OrderList.objects.filter(repairer_id=request.user, customer_id=data).values('pk','text_order', 'time_in').order_by('-time_in')[0:5]
    json_orders = json.dumps(list(orders), default=str)
    apartment=Apartment.objects.filter(owner=data).values('pk','name','address_city', 'address_street_app', 'address_num').order_by('-address_street_app')
    json_apartment = json.dumps(list(apartment), default=str)
    if orders.exists():
        return JsonResponse({'pk': data.pk,
                         'name':data.customer_name,
                         'phone':data.phone,
                         'telegram':data.telegram,
                         'foto': str(data.foto),
                         'profile': data.profile,
                         'orders': json_orders,
                         'apartment': json_apartment,
                         })
    else: return JsonResponse({'pk': 'None',})


# @login_required
# def listorder_for_order_list_paginator_json(request, **kwargs):
    """for ajax request """
    # data = OrderList.objects.filter(pk__lt=request.GET.get('last_pk'), repairer_id=request.user) \
    #            .select_related('apartment_id', 'customer_id') \
    #            .order_by('-pk') \
    #            .values('pk', 'time_in', 'text_order', 'customer_id__customer_name',
    #                    'customer_id__phone', 'customer_id__telegram',
    #                    'apartment_id__address_city', 'apartment_id__address_street_app',
    #                    'apartment_id__address_num', 'apartment_id__location_longitude',
    #                    'apartment_id__location_latitude')[0:14]
    # print(request.GET)
    # data = OrderList.objects.filter(pk__lt=request.GET.get('last_pk'), repairer_id=request.user) \
    #            .select_related('apartment_id', 'customer_id') \
    #            .order_by('-pk')
    #
    # filterset = OrderFilter(request.GET, data).qs.values('pk', 'time_in', 'text_order', 'customer_id__customer_name',
    #                    'customer_id__phone', 'customer_id__telegram',
    #                    'apartment_id__address_city', 'apartment_id__address_street_app',
    #                    'apartment_id__address_num', 'apartment_id__location_longitude',
    #                    'apartment_id__location_latitude')[0:14]
    #
    # json_data = json.dumps(list(filterset), default=str)
    # return JsonResponse(json_data, safe=False)


@login_required
def save_list_jobs(request, **kwargs):
    """for ajax request """
    FormSet_ = modelformset_factory(OrderList, fields=('text_order','apartment_id', 'customer_id'))

    formset = FormSet_(request.POST).save(commit=False)
    if formset:
        for instance in formset:
            if instance.text_order:
                instance.order_status = 'SND'
                instance.repairer_id = request.user
                instance.customer_id = UserProfile.objects.get(pk=request.POST.get('customer_id'))
                instance.save()
    return JsonResponse(request.GET, safe=False)


@login_required
def DeleteIvoiceService(request, **kwargs):
    """for ajax request """

    invoice_object = get_object_or_404(Invoice.objects.filter(order_id__repairer_id=request.user),
                                       pk=kwargs.get("invoice_pk"))
    invoice_object.delete()
    return JsonResponse({"message": "success"})


@login_required
def change_work_status(request, **kwargs):
    """for ajax request """
    b = get_object_or_404(OrderList, pk=request.GET.get("order_pk"))
    if request.GET.get('work_status') in ORDER_STATUS_FOR_CHECK and b.repairer_id == request.user:
        b.order_status = request.GET.get('work_status')
        if b.order_status == 'END': b.time_out = datetime.now()
        b.save()
        return JsonResponse({"message": request.GET.get('work_status'), "pk": request.GET.get("order_pk")})
    else:
        return JsonResponse({"message": "error"})


def input_street(request, **kwargs):
    """for ajax request """
    b = StreerTbilisi.objects.filter(name_street__istartswith=request.GET.get('street')) \
            .values('type_street', 'name_street')[0:15]
    json_data = json.dumps(list(b), default=str)
    return JsonResponse(json_data, safe=False)


def creat_order_from_owner_profile(request, **kwargs):
    b=OrderForm().save(commit=False)
    print(b)
    b.repairer_id=User.objects.get(pk=51)  #TODO add logic to set master
    b.customer_id=UserProfile.objects.get(pk=request.POST.get('customer_id'))
    b.apartment_id=Apartment.objects.get(pk=request.POST.get('apartment_id'))
    b.text_order = request.POST.get('text_order')
    b.save()

    return JsonResponse({"message": request.POST.get('name')})