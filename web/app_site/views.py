import json
import logging
import uuid
from itertools import count

from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db.models import Count, Subquery, F, Exists, OuterRef, Sum

from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.http import FileResponse, HttpResponseRedirect, JsonResponse, Http404
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .constants import *
from .exeptions import BaseClassExeption
from .filters import OrderFilter, ClientFilter, ApartmentFilter
from .forms import *
from .repository import DataFromRepairerList, DataFromOrderList, DataFromInvoice, DataFromUserProfile
from .serialaizers import StreetModelSerializer, OrderStatusSerializer, InvoiceSerializer, UserSerializer, \
    UpdateMasterSerializer
from .utils import *

from rest_framework import generics

logger = logging.getLogger('django')


class ApartmentList(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Apartment
    context_object_name = 'apart'
    template_name = 'repairer/apartments.html'
    permission_required = PERMISSION_FOR_REPAIER
    queryset = Apartment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('address_city') is not None:
            queryset = Apartment.objects.order_by('address_street_app').only('pk', 'address_city', 'address_street_app',
                                                                             'address_num').all()
        self.filterset = ApartmentFilter(self.request.GET, queryset)
        return self.filterset.qs


class ApartmentUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Apartment
    template_name = 'repairer/apartment_update.html'
    form_class = ApartentUpdateForm
    permission_required = PERMISSION_FOR_REPAIER
    success_url = '/apartments/?address_city=&address_street_app='


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


class Error404(TemplateView):
    template_name = '404.html'

class InfoTemplate(TemplateView):
    template_name = 'information.html'


class InvoiceCreate(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """ Add name of works, quantity, price to order  """
    model = OrderList
    context_object_name = 'info'
    template_name = 'repairer/invoice.html'
    permission_required = PERMISSION_FOR_REPAIER

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['invoice'] = DataFromInvoice().get_data_from_invoice_with_amount(order_id_=self.object.pk)
        context['type_work'] = WORK_CHOICES
        context['next'] = DataFromOrderList() \
            .get_next_number_for_paginator_from_OrderList(pk=self.object.pk)
        context['prev'] = DataFromOrderList() \
            .get_previous_number_for_paginator_from_OrderList(pk=self.object.pk)
        InvoiceFormSet = modelformset_factory(Invoice, form=InvoiceForm, extra=0)
        formset = InvoiceFormSet(queryset=Invoice.objects.none())
        context['form'] = formset                          # TODO refactor filter 3 is a group`s number 'repaier'
        context['list_masters'] = User.objects.filter(groups=3).values('pk', 'username',
                                                                       'groups')
        return context

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
        if self.request.user.is_authenticated:
            if self.request.user.groups.first().name == 'owner':
                per = UserProfile.objects.get(pk=1101)
                context['form_appart']=ApartmentFormOwner(person=per)


        context['form_customer'] = CustomerForm
        return context

    def form_valid(self, form):
        with (transaction.atomic()):
            if self.request.user.is_authenticated:
                if self.request.user.groups.first().name == 'owner' and self.request.POST.get('apartment_id') and self.request.POST.get('customer_id'):
                    form.instance.customer_id = UserProfile.objects.get(pk=self.request.POST.get('customer_id'))
                    form.instance.apartment_id = Apartment.objects.get(pk=self.request.POST.get('apartment_id'))
                    form.save()
                    return JsonResponse({'message': f'<h3>Заявка № {form.instance.pk} отправлена успешно!</h3>',
                                         'pk': form.instance.pk,
                                         'text': form.instance.text_order,
                                         'date': form.instance.time_in,
                                         'repaier': '',
                                         'apartment': form.instance.apartment_id.pk
                                         })
                elif self.request.user.groups.first().name == 'repairer':
                    customer = OrderCustomerForm(self.request.POST).save()
                    app = ApartmentForm(self.request.POST).save(commit=False)
                    app.owner = customer
                    app.save()
                    form.instance.apartment_id = app
                    form.instance.customer_id = customer
            else:
                customer = OrderCustomerForm(self.request.POST).save()
                app = ApartmentForm(self.request.POST).save(commit=False)
                app.owner = customer
                app.save()
                form.instance.apartment_id = app
                form.instance.customer_id = customer

            form.save()

            return JsonResponse({'message': f'<h2>Благодарим Вас за заявку!</h1><h3>Заявка № {form.instance.pk} отправлена успешно!</h2>',
                                 'contact': f'<h4>Ваш менеджер мастер Сергей: <br><img src="/media/masters/51.jpg" class="rounded-circle" width="100">.</h4>'
                                            f'<h5>Вы можете написать ему, уточнить детали, отправить фото работ или геопозицию:</h5>'
                                            f'<a class="mx-2" title="Telegram" href="https://t.me/+995598259119"><img src="/static/images/telegram.gif" width="50" alt="Telegram"></a>'
                                            f'<a class="mx-2" title="WhatsApp" href="https://wa.me/+79604458687"><img src="/static/images/whatsapp.png" width="55" alt="WhatsApp"></a>',
                                 'pk': form.instance.pk,
                                 'auth': self.request.user.is_authenticated
                                 })





class OrderDelete(BaseClassExeption, LoginRequiredMixin, DeleteView):
    model = OrderList
    template_name = 'order_delete.html'

    def get_success_url(self):
        dict_choice_url = {'repairer': '/list_order', 'owner': '/owner/apartment'}
        return dict_choice_url[self.request.user.groups.first().name]


class OwnerDetailInformation(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'owner/owner_profile.html'
    permission_required = PERMISSION_FOR_OWNER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prof'] = DataFromRepairerList().get_object_from_UserProfile(user=self.request.user)

        context['order_list_by_apartments'] = (
            OrderList.objects.only('time_in', 'text_order', 'apartment_id__address_street_app',
                                   'apartment_id__address_num', 'apartment_id__name', 'apartment_id__notes',
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
                                 .only('pk', 'address_city', 'address_street_app', 'address_num', 'foto', 'notes',
                                        'name')
                                 .order_by('address_street_app'))
        # detail info of apartments wich have no orders
        list_app_ = set([i.get('apartment_id') for i in context['order_list_by_apartments'].values('apartment_id')])
        list_app = context['apartments'].exclude(pk__in=list_app_)
        context['list_app'] = list_app
        return context

class OwnerInvoice(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """ list of all orders """
    model = OrderList
    context_object_name = 'info'
    template_name = 'owner/owner_invoice.html'
    permission_required = PERMISSION_FOR_OWNER

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['invoice'] = DataFromInvoice().get_data_from_invoice_with_amount(order_id_=self.object.pk)
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
                    .select_related('customer_id', 'apartment_id', 'repairer_id')
                    .values('pk', 'time_in', 'repairer_id__pk', 'repairer_id__username',
                            'text_order', 'apartment_id__address_city', 'apartment_id__name',
                          'apartment_id__address_street_app', 'apartment_id__address_num',
                            'customer_id__pk', 'customer_id__user', 'customer_id__customer_name'
                            ))
        self.filterset = OrderFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # c = context['filterset'].qs.values('pk')
        # c_ = DataFromInvoice().get_total_cost_of_some_orders(list_of_orders=c)
        # context['summ_orders'] = c_
        # context['count_orders'] = self.get_queryset().count()
        return context


class OrdersOnTheStreet(ListView):
    model = OrderList
    context_object_name = 'order'
    template_name = 'repairer/order_list.html'

    def get_queryset(self):
        queryset = (super().get_queryset()
                    .select_related('customer_id', 'apartment_id', 'repairer_id')
                    .filter(apartment_id__address_street_app__icontains=self.request.GET.get('street'))
                    .values('pk', 'time_in', 'repairer_id__pk', 'repairer_id__username',
                            'text_order', 'customer_id__pk',
                            'customer_id__customer_name', 'customer_id__phone',
                            'customer_id__telegram', 'customer_id__whatsapp',
                            'apartment_id__link_location', 'apartment_id__address_street_app',
                            'apartment_id__address_city', 'apartment_id__address_num'
                            ))
        return queryset


class OwnerOrderManagementSystem(OrderManagementSystem, BaseClassExeption, LoginRequiredMixin, ListView):
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


class OwnerApartmentCreate(BaseClassExeption, LoginRequiredMixin, CreateView):
    model = Apartment
    template_name = 'owner/apartment_update.html'
    form_class = ApartentUpdateForm
    success_url = '../apartment'

    def form_valid(self, form):
        super().form_valid(form)
        form.instance.owner = UserProfile.objects.get(user=self.request.user)
        form.save()
        return redirect('apartment')


class OwnerApartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Apartment
    template_name = 'owner/apartment_update.html'
    form_class = ApartentUpdateForm
    success_url = '../apartment'


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderUpdateForm

    def get_success_url(self):
        return '/list_order/' + str(self.object.pk)


class RepairerDetailInformation(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
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


class Statistica(BaseClassExeption, PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'repairer/statistica.html'
    model = OrderList
    context_object_name = 'order'
    ordering = ['-time_in']
    permission_required = PERMISSION_FOR_REPAIER

    def get_queryset(self):
        queryset = super().get_queryset().select_related('customer_id', 'apartment_id', 'repairer_id').all()
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
    template_name = 'account/login.html'
    def get_success_url(self):
        super().get_success_url()
        dict_choice_url = {'repairer': reverse_lazy('user', kwargs={'pk': self.request.user.pk}),
                           'owner': reverse_lazy('profile')}
        return dict_choice_url[self.request.user.groups.first().name]

class UserRegisterView(CreateView):
    """ Registration of repairer """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'account/register.html'

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.is_active = False
            self.object.save()
            my_group = Group.objects.get(name='owner')
            my_group.user_set.add(self.object)
            profile=UserProfile()
            profile.user = self.object
            profile.customer_name=uuid.uuid4
            profile.save()
            return redirect('message_after_registration')


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
def OrderAddRepaier(request):   # TODO refactor with serializers
    """Add the repairer to order using telegram-bot"""
    order = get_object_or_404(OrderList, pk=request.GET['pk_order'])
    repaier = get_object_or_404(User, pk=request.GET['pk_repairer'])
    if order and repaier:
        if not order.repairer_id:
            order.repairer_id = repaier
            order.order_status = 'SND'
            order.save()
            return redirect('home', args=(order.pk,))  # TODO настроить сообщение, что ремонтник уже указан
        else:
            return redirect('home')


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

    orders = OrderList.objects.filter(customer_id=data).values('pk', 'text_order', 'time_in').order_by('-time_in')[0:5]
    json_orders = json.dumps(list(orders), default=str)

    apartment = Apartment.objects.filter(owner=data).values('pk', 'name', 'address_city', 'address_street_app',
                                                            'address_num').order_by('-address_street_app')
    json_apartment = json.dumps(list(apartment), default=str)
    if orders.exists():
        return JsonResponse({'pk': data.pk,
                             'name': data.customer_name,
                             'phone': data.phone,
                             'telegram': data.telegram,
                             'foto': str(data.foto),
                             'profile': data.profile,
                             'orders': json_orders,
                             'apartment': json_apartment,
                             })
    else:
        return JsonResponse({'pk': 'None', })


@login_required
def save_list_jobs(request, **kwargs):
    """for ajax request """
    FormSet_ = modelformset_factory(OrderList, fields=('text_order', 'apartment_id', 'customer_id'))

    formset = FormSet_(request.POST).save(commit=False)
    if formset:
        for instance in formset:
            if instance.text_order:
                instance.order_status = 'SND'
                instance.customer_id = UserProfile.objects.get(pk=request.POST.get('customer_id'))
                instance.save()
    return JsonResponse(request.GET, safe=False)


class DeleteIvoiceServiceAPI(generics.DestroyAPIView):
    """API for ajax request """
    serializer_class = InvoiceSerializer
    http_method_names = ['delete']

    def get_queryset(self):
        queryset = Invoice.objects.all()
        return queryset


class StreetListApi(generics.ListAPIView):
    """API for ajax request """
    serializer_class = StreetModelSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = StreetTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:10]
        return queryset


class OrderStatusUpdateAPI(generics.UpdateAPIView):
    """API for ajax request """
    serializer_class = OrderStatusSerializer
    http_method_names = ['patch']

    def get_object(self):
        b = super().get_object()
        f = orderstat.index(b.order_status)
        try:
            index_list = orderstat[f+1]
        except IndexError:
            index_list = orderstat[0]
        b.order_status = index_list
        b.save()
        return b

    def get_queryset(self):
        queryset = OrderList.objects.all()
        return queryset


class MasterUpdateAPI(generics.UpdateAPIView):
    """API for ajax request """
    serializer_class = UpdateMasterSerializer
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        s = super().update(request, *args, **kwargs)
        try:
            z = self.get_object()
            resp = {'pk': z.pk, 'repairer_name': str(z.repairer_id), 'repairer_id': str(z.repairer_id.pk)}
            return JsonResponse(resp, safe=False)
        except Exception as e:       # TODO add  type`s exeption
            return s

    def get_queryset(self):
        queryset = OrderList.objects.all()
        return queryset


class MastersListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    http_method_names = ['get']

    def get_queryset(self):                 # TODO refactor filter 3 is a group`s number 'repaier'
        queryset = User.objects.filter(groups=3).values('pk', 'username', 'groups')
        return queryset


def creat_order_from_owner_profile(request, **kwargs):
    b = OrderForm().save(commit=False)
    b.repairer_id = User.objects.get(pk=51)  # TODO add logic to set master
    b.customer_id = UserProfile.objects.get(pk=request.POST.get('customer_id'))
    b.apartment_id = Apartment.objects.get(pk=request.POST.get('apartment_id'))
    b.text_order = request.POST.get('text_order')
    b.save()
    return JsonResponse({"message": request.POST.get('name')})

def verife_account(request):
    token_ = request.GET.get('token')
    print(token_)
    pk_=request.GET.get('pk')
    print(pk_)
    user_ = get_object_or_404(User, pk=pk_)
    profile = UserProfile.objects.get(user=user_)
    if profile.customer_name == token_:
        with transaction.atomic():
            user_.is_active=True
            user_.save()
            profile.customer_name=''
            profile.save()
        return redirect('confirm_registration')
    else:
        raise Http404("")


