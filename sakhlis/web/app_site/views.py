import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .exeptions import BaseClassExeption
from .filters import OrderFilter
from .models import *
from .forms import OrderForm, InvoiceForm, UserRegisterForm, RepairerForm
from .utils import *
from django.http import FileResponse, Http404, HttpResponseRedirect, JsonResponse
import io
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

class UserRegisterView(CreateView):
    """ Registration of repairer """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'


class UserDetailInformation(BaseClassExeption, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'repaier_update.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('')
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = RepairerList.objects.get(user=self.object)

        context['count'] =  OrderList.objects\
            .values('repairer_id')\
            .annotate(count=Count('repairer_id'))\
            .filter(repairer_id=self.request.user)

        context['sum'] = Invoice.objects\
            .values('order_id__repairer_id')\
            .annotate(count=Sum(F('price') * F('quantity')))\
            .filter(order_id__repairer_id=self.request.user)

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
                             'pk':form.instance.pk,
                             'auth': self.request.user.is_authenticated,
                               })


class OrderManagementSystem(BaseClassExeption, LoginRequiredMixin, ListView):
    """ list of all orders """
    model = OrderList
    context_object_name = 'order'
    template_name = 'order_list.html'

    def get_queryset(self):
        if not self.request.GET.get('work_status'):
            self.queryset = OrderList.objects\
                .filter(repairer_id=self.request.user)\
                .order_by("-pk")
        else:
            self.queryset = OrderList.objects \
                .filter(repairer_id=self.request.user, order_status=self.request.GET.get('work_status')) \
                .order_by("-pk")

        return self.queryset[0:14]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm
        return context



class OrderUpdate(LoginRequiredMixin, UpdateView):
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


class OrderDelete(LoginRequiredMixin, DeleteView):
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
        context['invoice'] = Invoice.objects\
                                    .filter(order_id=self.object.pk)\
                                    .select_related('service_id')\
                                    .defer('service_id__type')\
                                    .annotate(amount=F('price') * F('quantity'))

        InvoiceFormSet = modelformset_factory(Invoice, form=InvoiceForm, extra=0)
        formset = InvoiceFormSet(queryset=Invoice.objects.none())
        context['form'] = formset
        context['type_work'] = WORK_CHOICES
        context['next'] = OrderList.objects.filter(pk__gt=self.object.pk, repairer_id=self.request.user).values('pk').first()
        context['prev'] = OrderList.objects.filter(pk__lt=self.object.pk, repairer_id=self.request.user).order_by('-pk').values('pk').first()

        return context

    def get_queryset(self):
        return OrderList.objects.filter(repairer_id=self.request.user)

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

class Statistica(BaseClassExeption, LoginRequiredMixin, TemplateView):
    template_name = 'statistica.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        a = OrderList.objects\
            .values('time_in__month', 'time_in__year')\
            .annotate(count=Sum(F('invoice__price') * F('invoice__quantity')))\
            .filter(repairer_id=self.request.user)\
            .order_by('time_in__year')
        print(a)

        b = OrderList.objects\
            .values('time_in__month', 'time_in__year')\
            .annotate(count=Count(F('pk')))\
            .filter(repairer_id=self.request.user)\
            .order_by('time_in__year')

        c = Invoice.objects \
            .values('service_id__type') \
            .annotate(count=Count(F('service_id__type'))) \
            .order_by('-count') \
            .filter(order_id__repairer_id=self.request.user)

        c_ = Invoice.objects \
            .values('service_id__type') \
            .annotate(count=Sum(F('price') * F('quantity'))) \
            .order_by('-count') \
            .filter(order_id__repairer_id=self.request.user)


        h = OrderList.objects \
            .values('time_in__date') \
            .annotate(count=Sum(F('invoice__price') * F('invoice__quantity'))) \
            .order_by('-time_in__date') \
            .filter(repairer_id=self.request.user)[0:30:-1]


        labels, sizes = get_data_for_graph(c,'service_id__type','count', WORK_CHOICES_)
        instans_graf=Graph(labels, sizes, 'Структура заказов, кол.', '')
        context['d']=instans_graf.make_graf_pie()

        labels, sizes = get_data_for_graph(c_, 'service_id__type', 'count', WORK_CHOICES_)
        instans_graf = Graph(labels, sizes, 'Структура заказов, лар.', '')
        context['d_'] = instans_graf.make_graf_pie()

        labels, sizes = get_data_for_graph(a,'time_in__month','count', MONTH_)
        instans_graf = Graph(labels, sizes, 'Выручка', 'lar')
        context['f'] = instans_graf.make_graf_bar()

        labels, sizes = get_data_for_graph(b,'time_in__month','count', MONTH_)
        instans_graf = Graph(labels, sizes, 'Количество заказов', 'кол')
        context['g'] = instans_graf.make_graf_bar()
        #
        labels, sizes = get_data_for_graph(h,'time_in__date','count')
        instans_graf = Graph(labels, sizes, 'Динамика за 30 дней.', '')
        context['hh'] = instans_graf.make_graf_plot()

        return context

class RepaierUpdate(BaseClassExeption, UpdateView):
    model = RepairerList
    template_name = 'repaier_create.html'
    form_class = RepairerForm

    def get_success_url(self):
        return '/user/' + str(self.request.user.pk)

def CreateIvoicePDF(request, **kwargs):
    """ Create invoice pdf-file for printing """

    # get information from models
    order_pk = kwargs.get("order_pk")
    info = get_info_for_pdf().get(pk=order_pk)
    # create file
    buf = io.BytesIO()
    doc = InvoiceMaker(buf, info)
    doc.createDocument()
    doc.savePDF()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'Invoice_{order_pk}_.pdf')


class OrderSearchForm(BaseClassExeption, LoginRequiredMixin, ListView):
    model = OrderList
    context_object_name = 'order'
    template_name = 'ordersearchform.html'
    ordering = ['-time_in']
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        b=self.request.GET.copy()
        b.__setitem__('repairer_id', self.request.user.pk)
        self.filterset = OrderFilter(b, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['form'] = OrderForm
        return context

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
                        .values('pk', 'time_in', 'text_order', 'customer_name', 'customer_phone', 'customer_telegram',
                                'address_city', 'address_street_app', 'address_num', 'location_longitude', 'location_latitude')[0:14]
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
    b = StreerTbilisi.objects.filter(name_street__istartswith=request.GET.get('street')).values('type_street', 'name_street')[0:15]
    json_data = json.dumps(list(b), default=str)
    return JsonResponse(json_data, safe=False)


# def geo_map(request, **kwargs):
#     """ """
#     b = OrderList.objects.all()
#     for a in b:
#
#         location = set_coordinates_address(a.address_street_app, 'Тбилиси', a.address_num)
#         if location != None:
#             a.location_longitude = float(location[0])
#             a.location_latitude = float(location[1])
#             a.save()
#     return JsonResponse({"message": "successful"})