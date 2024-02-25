import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .constants import *
from .exeptions import BaseClassExeption
from .filters import OrderFilter
from .models import *
from .forms import OrderForm, InvoiceForm, UserRegisterForm, RepairerForm
from .repository import DataFromRepairerList, DataFromOrderList, DataFromInvoice
from .utils import *

logger = logging.getLogger(__name__)


class UserRegisterView(BaseClassExeption, CreateView):
    """ Registration of repairer """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'account/register.html'


class UserDetailInformation(BaseClassExeption, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'repaier_update.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('')
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = DataFromRepairerList().get_object_from_RepairerList(user=self.object)
        context['count'] = DataFromOrderList().get_number_of_orders_from_OrderList(repairer=self.request.user)
        context['sum'] = DataFromInvoice().get_amount_money_of_orders(repairer=self.request.user)
        return context


class OrderCreate(BaseClassExeption, CreateView):
    """" Add order """
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.repairer_id = self.request.user
            form.instance.order_status = 'SND'
        form.save()
        return JsonResponse({'message': f'<h3>Заявка № {form.instance.pk} отправлена успешно!</h3>',
                                  'pk': form.instance.pk,
                                'auth': self.request.user.is_authenticated
                             })


class OrderManagementSystem(BaseClassExeption, LoginRequiredMixin, ListView):
    """ list of all orders """
    model = OrderList
    context_object_name = 'order'
    template_name = 'order_list.html'

    def get_queryset(self):
        if not self.request.GET.get('work_status'):
            self.queryset = DataFromOrderList() \
                .get_data_from_OrderList_all(repairer=self.request.user)
        else:
            self.queryset = DataFromOrderList() \
                .get_data_from_OrderList_with_order_status(repairer=self.request.user,
                                                           status_of_order=self.request.GET.get('work_status'))
        return self.queryset[0:14]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm
        return context


class OrderUpdate(BaseClassExeption, LoginRequiredMixin, UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_in'] = self.object.time_in
        context['pk'] = self.object.pk
        return context
    def get_success_url(self):
        return '/list_order/'+str(self.object.pk)


class OrderDelete(BaseClassExeption, LoginRequiredMixin, DeleteView):
    model = OrderList
    template_name = 'order_delete.html'
    success_url = '/list_order'


class InvoiceCreate(BaseClassExeption, LoginRequiredMixin, DetailView):
    """ Add name of works, quantity, price to order  """
    model = OrderList
    context_object_name = 'info'
    template_name = 'invoice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['invoice'] = DataFromInvoice().get_data_from_Invoice_with_amount(order_id_=self.object.pk)
        context['type_work'] = WORK_CHOICES
        context['next'] = DataFromOrderList()\
            .get_next_number_for_paginator_from_OrderList(repairer=self.request.user, pk=self.object.pk)
        context['prev'] = DataFromOrderList()\
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


class Error404(TemplateView):
    template_name = '404.html'



class Statistica(BaseClassExeption, LoginRequiredMixin, ListView):
    template_name = 'statistica.html'
    model = OrderList
    context_object_name = 'order'
    ordering = ['-time_in']

    def get_queryset(self):
        queryset = super().get_queryset()
        b = self.request.GET.copy()
        b.__setitem__('repairer_id', self.request.user.pk)
        self.filterset = OrderFilter(b, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)



        context['filterset'] = self.filterset

        queryset_from_OrderList=self.filterset.qs

        list_objects_from_OrderList=list(queryset_from_OrderList)

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
                            'time_in__month',  'count', MONTH_, 'Order`s quantity', 'quantity') \
                        .make_graf_bar()

        context['hh'] = Graph(data_from_oder.get_dayly_cost_of_orders(repairer=self.request.user),
                            'time_in__date', 'count', None, 'Dynamics', '') \
                        .make_graf_plot()
        return context




class OrderSearchForm(BaseClassExeption, LoginRequiredMixin, ListView):
    model = OrderList
    context_object_name = 'order'
    template_name = 'ordersearchform.html'
    ordering = ['-time_in']

    def get_queryset(self):
        queryset = super().get_queryset()
        b = self.request.GET.copy()
        b.__setitem__('repairer_id', self.request.user.pk)
        self.filterset = OrderFilter(b, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['form'] = OrderForm
        c = DataFromInvoice().get_total_cost_of_some_orders(list_of_orders=self.get_queryset())
        context['summ_orders'] = c.get('Summ')
        context['count_orders'] = self.get_queryset().count()
        return context


















class RepaierUpdate(BaseClassExeption, UpdateView):
    model = Repairer
    template_name = 'repaier_create.html'
    form_class = RepairerForm

    def get_success_url(self):
        return '/user/' + str(self.request.user.pk)


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
    """Add the repairer to order from telegram"""
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
def listservices_for_invoice_json(request, **kwargs):
    """for ajax request """
    data = Service.objects.filter(type=request.GET.get('type_work')).values('id', 'name')
    json_data = json.dumps(list(data))
    return JsonResponse(json_data, safe=False)


@login_required
def listorder_for_order_list_paginator_json(request, **kwargs):
    """for ajax request """
    data = OrderList.objects.filter(pk__lt=request.GET.get('last_pk'), repairer_id=request.user)\
                            .order_by('-pk')\
                            .values('pk', 'time_in', 'text_order', 'customer_name',
                                    'customer_phone', 'customer_telegram',
                                    'address_city', 'address_street_app',
                                    'address_num', 'location_longitude', 'location_latitude')[0:14]
    json_data = json.dumps(list(data), default=str)
    return JsonResponse(json_data, safe=False)


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
        b.save()
        return JsonResponse({"message": request.GET.get('work_status'), "pk": request.GET.get("order_pk")})
    else:
        return JsonResponse({"message": "error"})


def input_street(request, **kwargs):
    """for ajax request """
    b = StreerTbilisi.objects.filter(name_street__istartswith=request.GET.get('street')) \
                             .values('type_street', 'name_street')[0:15]
    json_data = json.dumps(list(b), default=str)
    print(JsonResponse(json_data, safe=False))
    return JsonResponse(json_data, safe=False)
