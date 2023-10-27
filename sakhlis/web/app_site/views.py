import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F, Prefetch, Sum, Count, Avg
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import OrderForm, InvoiceForm, UserRegisterForm, RepairerForm
from .utils import InvoiceMaker, get_data_for_graf, Graph, get_info_for_pdf
from django.http import FileResponse, Http404, HttpResponseRedirect, JsonResponse
import io


class UserRegisterView(CreateView):
    """ Registration of repairer """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        with transaction.atomic():            # todo check transaction
            super().post(request, *args, **kwargs)
            RepairerList.objects.create(user=self.object)
        return redirect('home')

class UserDetailInformation(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'repaier_update.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('')
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = RepairerList.objects.annotate(raiting=F('rating_sum')/F('rating_num'))\
            .get(user=self.object)

        context['count'] =  OrderList.objects\
            .values('repairer_id')\
            .annotate(count=Count('repairer_id'))\
            .filter(repairer_id=self.request.user)

        context['sum'] = Invoice.objects\
            .values('order_id__repairer_id')\
            .annotate(count=Sum(F('price') * F('quantity')))\
            .filter(order_id__repairer_id=self.request.user)

        return context


class OrderCreate(CreateView):
    """" Add order """
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return JsonResponse({'message': f'<h3>Заявка № {self.object.pk} отправлена успешно!</h3>',
                             'pk':self.object.pk,
                             'text_order': self.object.text_order,
                             'time_in': self.object.time_in,
                             'customer_name':self.object.customer_name,
                             'customer_phone': self.object.customer_phone,
                             'customer_telegram': self.object.customer_telegram,
                             'address_city': self.object.address_city,
                             'address_street_app': self.object.address_street_app,
                             'address_num': self.object.address_num,
                             })

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.repairer_id = self.request.user
            form.instance.order_status = 'SND'

        name_telegram_customer = form.instance.customer_telegram.replace('@', '').replace('+', '')\
            .replace('-', '')


        if name_telegram_customer.isdigit():
            form.instance.customer_telegram='+' + name_telegram_customer
        else:
            form.instance.customer_telegram = name_telegram_customer

        form.instance.text_order = form.instance.text_order.replace('<', '[').replace('>', ']')

        return super(OrderCreate, self).form_valid(form)


class OrderManagementSystem(LoginRequiredMixin, ListView):
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



def OrderAddRepaier(request):
    """Add the repairer to order from telegram"""
    if request.GET:
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
    else:
        raise Http404()


class InvoiceCreate(LoginRequiredMixin, DetailView):
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
        context['next'] = OrderList.objects.filter(pk__gt=self.object.pk).values('pk').first()
        context['prev'] = OrderList.objects.filter(pk__lt=self.object.pk).order_by('-pk').values('pk').first()

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



class Statistica(LoginRequiredMixin, TemplateView):
    template_name = 'statistica.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        a = OrderList.objects\
            .values('time_in__month', 'time_in__year')\
            .annotate(count=Sum(F('invoice__price') * F('invoice__quantity')))\
            .filter(repairer_id=self.request.user)

        b = OrderList.objects\
            .values('time_in__month', 'time_in__year', 'pk')\
            .annotate(count=Avg(F('invoice__price') * F('invoice__quantity')))\
            .filter(repairer_id=self.request.user)

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


        labels, sizes = get_data_for_graf(c,'service_id__type','count', WORK_CHOICES_)
        instans_graf=Graph(labels, sizes, 'Структура заказов, кол.', '')
        context['d']=instans_graf.make_graf_pie()

        labels, sizes = get_data_for_graf(c_, 'service_id__type', 'count', WORK_CHOICES_)
        instans_graf = Graph(labels, sizes, 'Структура заказов, лар.', '')
        context['d_'] = instans_graf.make_graf_pie()

        labels, sizes = get_data_for_graf(a,'time_in__month','count', MONTH_)
        instans_graf = Graph(labels, sizes, 'Выручка', 'lar')
        context['f'] = instans_graf.make_graf_bar()

        labels, sizes = get_data_for_graf(b,'time_in__month','count', MONTH_)
        instans_graf = Graph(labels, sizes, 'Средний чек заказа', 'кол')
        context['g'] = instans_graf.make_graf_bar()

        labels, sizes = get_data_for_graf(h,'time_in__date','count')
        instans_graf = Graph(labels, sizes, 'Динамика за 30 дней.', '')
        context['hh'] = instans_graf.make_graf_plot()


        return context



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


def listservices_for_invoice_json(request, **kwargs):
    """for ajax request """
    if request.user.is_authenticated:
        data = Service.objects.filter(type=request.GET.get('type_work')).values('id', 'name')
        json_data = json.dumps(list(data))
        return JsonResponse(json_data, safe=False)

def listorder_for_order_list_paginator_json(request, **kwargs):
    """for ajax request """
    if request.user.is_authenticated:
        data = OrderList.objects.filter(pk__lt=request.GET.get('last_pk'), repairer_id=request.user)\
                            .order_by('-pk')\
                            .values('pk', 'time_in', 'text_order', 'customer_name', 'customer_phone', 'customer_telegram',
                                    'address_city', 'address_street_app', 'address_num')[0:14]
        json_data = json.dumps(list(data), default=str)
        return JsonResponse(json_data, safe=False)

def DeleteIvoiceService(request, **kwargs):
    """for ajax request """
    if request.user.is_authenticated:
        invoice_object = get_object_or_404(Invoice.objects.filter(order_id__repairer_id=request.user),
                              pk=kwargs.get("invoice_pk"))
        invoice_object.delete()
        return JsonResponse({"message": "success"})

def change_work_status(request, **kwargs):
    """for ajax request """
    if request.user.is_authenticated:
        b = get_object_or_404(OrderList, pk=request.GET.get("order_pk"))
        if request.GET.get('work_status') in ORDER_STATUS_FOR_CHECK and b.repairer_id == request.user:
            b.order_status = request.GET.get('work_status')
            b.save()
            return JsonResponse({"message": request.GET.get('work_status')})
        else:
            return JsonResponse({"message": "error"})

class RepaierUpdate(UpdateView):
    model = RepairerList
    template_name = 'repaier_create.html'
    form_class = RepairerForm

    def get_success_url(self):
        return '/user/' + str(self.request.user.pk)