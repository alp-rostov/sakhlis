from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.files.storage import DefaultStorage
from django.db.models import F, Prefetch, Count, Sum
from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from formtools.wizard.views import SessionWizardView

from .models import RepairerList, OrderList, Invoice
from .filters import RepFilter, OrderFilter
from .forms import OrderForm, InvoiceForm, UserRegisterForm, RepairerForm
from .utils import InvoiceMaker
from django.http import FileResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponse
import io


# ___________________________________________________________________________________________________________________
def get_info1(spk: int):
    return OrderList.objects.get(pk=spk)


def get_info2():
    return OrderList.objects \
        .annotate(sum=Sum(F('invoice__price') * F('invoice__quantity'))) \
        .prefetch_related(Prefetch('invoice_set', Invoice.objects
                                   .defer('quantity_type', 'service_id__type')
                                   .select_related('service_id')
                                   .annotate(sum=F('price') * F('quantity')))
                          ).select_related('repairer_id')
    # .defer('customer_code', 'repairer_id__phone', 'repairer_id__city',
    #        'repairer_id__foto','repairer_id__rating_sum', 'repairer_id__rating_num')


# __________________________________________________________________________________________________________________


class RepairerL(LoginRequiredMixin, ListView):
    """ List of repairman """
    model = RepairerList
    context_object_name = 'repairer'
    template_name = 'repairer_list.html'
    queryset = RepairerList.objects \
        .select_related('user') \
        .all() \
        .values('city', 'phone', 'foto', 'user', 'user__last_name', 'user__first_name', 'user__email')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RepFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class UserRegisterView(CreateView):
    """ Registration of repairman """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'

    def get_success_url(self):
        c=User.objects.get(username=self.form_class.username)
        print(c.pk)
        return 'home'


class UserUpdate(DetailView):
    model = User
    template_name = 'repaier_update.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('')

    # def get_form(self, form_class=None):
    #     UserForm = RepairerForm(initial = RepairerList.objects.get(user=77))
    #
    #     return UserForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['UserForm'] = RepairerForm(initial = RepairerList.objects.get(user=77))
        print(RepairerForm(RepairerList.objects.get(user=77)))
        return context


    # def post(self, formset, **kwargs):
    #     b = get_info1(self.kwargs.get('order_pk'))
    #     AuthorFormSet = modelformset_factory(Invoice, fields='__all__')
    #     formset = AuthorFormSet(self.request.POST)
    #     instances = formset.save(commit=False)
    #     for instance in instances:
    #         instance.order_id = b
    #         instance.save()
    #     return HttpResponseRedirect(reverse('list_detail', args=(self.kwargs.get("order_pk"),)))

class OrderCreate(CreateView):
    """" Adding a repair order """
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')


class OrderManagementSystem(ListView):
    """ list of all repair orders with Invoices"""

    model = OrderList
    context_object_name = 'order'
    template_name = 'order_list.html'
    ordering = ['-time_in']
    queryset = get_info2().select_related('repairer_id')

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

    # queryset = get_info2().select_related('repairer_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repairer'] = RepairerList.objects.all()
        return context


class OrderUpdate(UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderForm
    success_url = reverse_lazy('list_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_in'] = self.object.time_in
        context['pk'] = self.object.pk
        return context


class OrderDelete(DeleteView):
    model = OrderList
    template_name = 'order_delete.html'
    success_url = reverse_lazy("list_order")


@require_http_methods(["GET"])
def OrderAddRepaier(request):
    """Aad the repaier to order from telegram"""
    if request.GET:
        order = get_info1(request.GET['pk_order'])
        repaier = RepairerList.objects.get(pk=request.GET['pk_repairer'])
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


class InvoiceCreate(FormView):
    """ Create Invoice for payment """

    template_name = 'invoice.html'
    context_object_name = 'invoice'

    def get_form(self, form_class=None):
        InvoiceFormSet = modelformset_factory(Invoice, form=InvoiceForm, exclude=('order_id',), extra=0)
        formset = InvoiceFormSet(queryset=Invoice.objects
                                 .filter(order_id=self.kwargs.get('order_pk'))
                                 .select_related('service_id')
                                 .defer('service_id__type'))

        return formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['info'] = get_info1(self.kwargs.get('order_pk'))
        return context

    def post(self, formset, **kwargs):
        b = get_info1(self.kwargs.get('order_pk'))
        AuthorFormSet = modelformset_factory(Invoice, fields='__all__')
        formset = AuthorFormSet(self.request.POST)
        instances = formset.save(commit=False)
        for instance in instances:
            instance.order_id = b
            instance.save()
        return HttpResponseRedirect(reverse('list_detail', args=(self.kwargs.get("order_pk"),)))


@require_http_methods(["GET"])
def DeleteIvoiceService(request, **kwargs):
    if request.user.is_authenticated:
        Invoice.objects.get(pk=kwargs.get("invoice_pk")).delete()

    return HttpResponseRedirect(reverse('invoice', args=(kwargs.get("order_pk"),)))


class Statistica(TemplateView):
    template_name = 'statistica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['a'] = OrderList.objects.values('time_in__month', 'time_in__year').annotate(sum=Sum(F('price')))
        context['b'] = OrderList.objects.values('repairer_id__last_name').annotate(sum=Sum(F('price')),
                                                                                   con=Count(F('id')))

        return context


@require_http_methods(["GET"])
def CreateIvoicePDF(request, **kwargs):
    """ Create invoice pdf-file for printing """

    # get information from models
    order_pk = kwargs.get("order_pk")
    info = get_info2().get(pk=order_pk)
    # create file
    buf = io.BytesIO()
    doc = InvoiceMaker(buf, info)
    doc.createDocument()
    doc.savePDF()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'Invoice_{order_pk}_.pdf')


class RepaiermanSpace(LoginRequiredMixin, DetailView):
    """ Settings личный кабинет"""

    template_name = 'repaierman.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['order'] = get_info2().get()
        return context
