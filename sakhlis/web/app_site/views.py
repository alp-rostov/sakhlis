from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from requests import request

from .models import RepairerList, OrderList, Invoice, Service
from .filters import RepFilter, OrderFilter
from .forms import RepairerForm, BaseRegisterForm, OrderForm, InvoiceForm


class RepairerL(LoginRequiredMixin, ListView):
    model = RepairerList
    context_object_name = 'repairer'
    template_name = 'repairer_list.html'
    queryset = RepairerList.objects.all().order_by('s_name').values('s_name', 'city', 'name',
                                                                    'phone', 'email', 'foto', 'pk')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RepFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class RepaierD(DetailView):
    model = RepairerList
    template_name = 'repaier_detail.html'
    context_object_name = 'rep'


class RepaierCreate(LoginRequiredMixin, CreateView):
    model = RepairerList
    template_name = 'repaier_create.html'
    form_class = RepairerForm


class RepaierUpdate(UpdateView):
    model = RepairerList
    template_name = 'repaier_create.html'
    form_class = RepairerForm


class RepaierDelete(DeleteView):
    model = RepairerList
    template_name = 'repaier_delete.html'
    success_url = '/app'


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class OrderCreate(CreateView):
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = '/'


class OrderManagementSystem(ListView):
    model = OrderList
    context_object_name = 'order'
    template_name = 'order_list.html'
    ordering = ['-time_in']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = OrderFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class OrderDatail(DetailView):
    model = OrderList
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.object.invoice_set.all().\
            annotate(min_price=F('price')*F('quantity'))
        context['sum'] = sum(i.min_price for i in context['services'])
        return context



class OrderUpdate(UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderForm
    success_url = '/list_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ServicesFormSet = inlineformset_factory(Service, Invoice, form=ServiceForm, fields='__all__', fk_name='service_id', extra=1)
        queryset_ = Service.objects.get(pk='8')
        print(queryset_)
        b = ServicesFormSet(instance=queryset_)
        pprint(b)
        context['ServiceForm'] = b

        if self.request.POST:
            pass
        else:
            pass
            # context['ServiceForm'] = ServiceForm()
            # context['formset'] = ServicesFormSet(queryset=Service.objects.filter(order_id={self.kwargs["pk"]}))
            # print(context['formset'])
        return context


class OrderDelete(DeleteView):
    model = OrderList
    template_name = 'order_delete.html'
    success_url = '/list_order'

@require_http_methods(["GET"])
def OrderAddRepaier(request):
    order = OrderList.objects.get(pk=request.GET['pk_order'])
    repaier = RepairerList.objects.get(pk=request.GET['pk_repairer'])
    if order and repaier:
        if not order.repairer_id:
            order.repairer_id = repaier
            order.save()
            return redirect(f'/list_order/{order.pk}')
        else:
            return redirect(f'/')  # TODO настроить сообщение, что ремонтник уже указан


class InvoiceCreate(CreateView):
    model = Invoice
    template_name = 'invoice.html'
    context_object_name = 'invoice'
    form_class = InvoiceForm

    def form_valid(self, form,  **kwargs):
        invoice = form.save(commit=False)
        invoice.order_id = OrderList.objects.get(pk=self.kwargs['order_pk'])
        invoice.save()
        return redirect(f'/list_order/{self.kwargs["order_pk"]}')