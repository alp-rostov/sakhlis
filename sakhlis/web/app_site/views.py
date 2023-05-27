from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F, Prefetch, Count, Sum
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import RepairerList, OrderList, Invoice, Service
from .filters import RepFilter, OrderFilter
from .forms import RepairerForm, BaseRegisterForm, OrderForm, InvoiceForm

class RepairerL(LoginRequiredMixin, ListView):
    model = RepairerList
    context_object_name = 'repairer'
    template_name = 'repairer_list.html'
    queryset = RepairerList.objects \
        .all() \
        .order_by('s_name') \
        .values('s_name', 'city', 'name', 'phone', 'email', 'foto', 'pk')

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
    queryset = OrderList.objects \
        .all() \
        .select_related('repairer_id') \
        .prefetch_related(Prefetch('invoice_set', Invoice.objects
                                   .all()
                                   .select_related('service_id')))

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
    queryset = OrderList.objects \
        .annotate(sum=Sum(F('invoice__price') * F('invoice__quantity')))\
        .select_related('repairer_id') \
        .prefetch_related(Prefetch('invoice_set', Invoice.objects
                                   .all()
                                   .select_related('service_id').annotate(sum=F('price') * F('quantity'))))


class OrderUpdate(UpdateView):
    model = OrderList
    template_name = 'order_update.html'
    form_class = OrderForm
    success_url = '/list_order'


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


class InvoiceCreate(FormView):
    template_name = 'invoice.html'
    context_object_name = 'invoice'

    def get_form(self, form_class=None):
        AuthorFormSet = modelformset_factory(Invoice, exclude=('order_id',))
        formset=AuthorFormSet(queryset=Invoice.objects.filter(order_id=self.kwargs.get('order_pk')))
        return formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['info'] = OrderList.objects.get(pk=self.kwargs.get('order_pk'))
        return context

    def post(self, formset, **kwargs):
        b=OrderList.objects.get(pk=self.kwargs.get('order_pk'))
        AuthorFormSet = modelformset_factory(Invoice, fields='__all__')
        formset = AuthorFormSet(self.request.POST)
        instances = formset.save(commit=False)
        for instance in instances:
            instance.order_id = b
            instance.save()
        return redirect(f'/list_order/{self.kwargs.get("order_pk")}')


class Statistica(TemplateView):
    template_name = 'statistica.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # context['b']=OrderList.objects.all().exclude(time_out=None).order_by('-time_in').annotate(sum=Sum(F('invoice__price') * F('invoice__quantity')))
        context['a'] = OrderList.objects.values('time_in__date').annotate(sum=Sum(F('price')))
        context['b'] = OrderList.objects.values('repairer_id__name').annotate(sum=Sum(F('price')), con=Count(F('id')))

        return  context
