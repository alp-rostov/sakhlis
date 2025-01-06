import json
import logging
import uuid

from PIL.ImageFont import ImageFont
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse, Http404, HttpResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView

from clients.filters import ClientFilter
from clients.form import CustomerForm, CustomerFormForModal
from .constants import *
from .exeptions import BaseClassExeption
from .filters import OrderFilter, ApartmentFilter
from .forms import *
from .repository import DataFromOrderList, DataFromInvoice
from .serialaizers import OrderStatusSerializer, InvoiceSerializer, UserSerializer, UpdateMasterSerializer
from .utils import *
from rest_framework import generics

logger = logging.getLogger('django')


class ApartmentList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
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

class Error404(TemplateView):
    template_name = '404.html'

class InfoTemplate(TemplateView):
    template_name = 'information.html'

class Clients(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """ LIST OF CLIENTS """
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


class InvoiceCreate(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
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
        context['list_masters'] = User.objects.filter(groups=2).values('pk', 'username',
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


class OrderCreate(CreateView):
    """" Add order """
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_appart'] = ApartmentForm
        context['form_customer'] = CustomerForm
        if self.request.user.is_authenticated and self.request.user.groups.first().name == 'owner':
            user_ = get_object_or_404(UserProfile, user=self.request.user)
        elif ((not self.request.user.is_authenticated or self.request.user.is_superuser)
              and is_valid_uuid(self.request.GET.get('qrcode'))):
            try:
                user_ = UserProfile.objects.get(qrcode_id=self.request.GET.get('qrcode'))
            except UserProfile.DoesNotExist:
                return context
        else:
            return context
        context['form_appart'] = ApartmentFormOwner(person=user_)
        context['form_customer'] = ''
        context['form_for_modal'] = CustomerFormForModal
        context['contact_data'] = coding_personal_data(name=str(user_),  phone=user_.phone, whatsapp=user_.whatsapp,
                                                       telegram=user_.telegram)
        context['qruuid'] =f'?qrcode={self.request.GET.get("qrcode")}'
        return context

    def form_valid(self, form):
        with (transaction.atomic()):
            if self.request.user.is_authenticated and self.request.user.groups.first().name == 'owner':
                customer_id = UserProfile.objects.get(user=self.request.user.id)
                apartment_id = Apartment.objects.get(pk=self.request.POST.get('apartment_id'))
                form.instance.apartment_id = apartment_id
                form.instance.customer_id = customer_id
                form.save()
                return JsonResponse({'message': f'<h3>Заявка № {form.instance.pk} отправлена успешно!</h3>',
                                     'pk': form.instance.pk,
                                     'text': form.instance.text_order,
                                     'date': form.instance.time_in,
                                     'repaier': '',
                                     'apartment': form.instance.apartment_id.pk
                                     })
            elif self.request.GET.get('qrcode'):
                apartment_id = Apartment.objects.get(pk=self.request.POST.get('apartment_id'))  #TODO eliminate code duplication
                customer_id = apartment_id.owner

            else:
                customer_id = OrderCustomerForm(self.request.POST).save()
                apartment_id = ApartmentForm(self.request.POST).save(commit=False)
                apartment_id.owner = customer_id
                apartment_id.save()

            form.instance.apartment_id = apartment_id
            form.instance.customer_id = customer_id
            form.save()

            response_ = {'message': f'{form.instance.pk}',
                         'contact': f'<h4>Ваш менеджер мастер Сергей: <br><img src="/media/masters/51.jpg" class="rounded-circle" width="100">.</h4>'
                                    f'<h5>Вы можете написать ему, уточнить детали, отправить фото работ или геопозицию:</h5>'
                                    f'<a class="mx-2" title="Telegram" href="https://t.me/+995598259119"><img src="/static/images/telegram.gif" width="50" alt="Telegram"></a>'
                                    f'<a class="mx-2" title="WhatsApp" href="https://wa.me/+79604458687"><img src="/static/images/whatsapp.png" width="55" alt="WhatsApp"></a>',
                         'pk': form.instance.pk,
                         'auth': self.request.user.is_authenticated
                         }
            return JsonResponse(response_)


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = OrderList
    template_name = 'order_delete.html'

    def get_success_url(self):
        dict_choice_url = {'repairer': '/list_order', 'owner': '/owner/apartment'}
        return dict_choice_url[self.request.user.groups.first().name]


class OrderManagementSystem(LoginRequiredMixin, ListView):
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


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderUpdateForm

    def get_success_url(self):
        return '/list_order/' + str(self.object.pk)


class RepairerDetailInformation(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'repairer/repaier_profile.html'
    permission_required = PERMISSION_FOR_REPAIER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_order'] = OrderForm
        context['form_appart'] = ApartmentForm
        context['form_customer'] = CustomerForm               # TODO refactor filter 2 is a group`s number 'repaier'
        context['list_masters'] = User.objects.filter(groups=2).values('pk', 'username', 'groups')
        context['orders'] = DataFromOrderList().get_data_from_OrderList_with_order_status(repairer=self.request.user,
                                                                                          status_of_order=['SND',
                                                                                                           'RCV'])
        return context


class RepaierUpdate(PermissionRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'repairer/repaier_create.html'
    form_class = CustomerForm
    permission_required = PERMISSION_FOR_REPAIER

    def get_success_url(self):
        return '/user/' + str(self.request.user.pk)


class Statistica(PermissionRequiredMixin, LoginRequiredMixin, ListView):
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


def create_qr_code_pdf(request, **kwargs):
    """ Create pdf-file for printing """
    buf = io.BytesIO()
    qrcode_id=request.GET.get('qrcode')
    doc = CreatePDF(buf, info_client=qrcode_id, info_order=None )
    doc.create_qr_code_client()
    doc.savePDF()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'QrCode_.pdf')


def CreateIvoicePDF(request, **kwargs):
    """ Create invoice pdf-file for printing """
    # get information from models
    order_pk = kwargs.get("order_pk")
    info = DataFromOrderList().get_all_data_of_order_with_from_invoice().get(pk=order_pk)
    # create file
    buf = io.BytesIO()
    doc = CreatePDF(buf, info_order=info)
    doc.createDocument_invoice()
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
        # queryset = User.objects.filter(groups=3).values('pk', 'username', 'groups')
        queryset = User.objects.values('pk', 'username', 'groups')
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
    pk_=request.GET.get('pk')
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