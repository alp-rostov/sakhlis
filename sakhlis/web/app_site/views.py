from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F, Prefetch, Sum
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import RepairerList, OrderList, Invoice
from .filters import RepFilter
from .forms import OrderForm, InvoiceForm, UserRegisterForm, RepairerForm
from .utils import InvoiceMaker
from django.http import FileResponse, Http404, HttpResponseRedirect, JsonResponse
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


class UserUpdate(DetailView):
    model = User
    template_name = 'repaier_update.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['UserForm'] = RepairerForm(initial = RepairerList.objects.get(user=77))
        print(RepairerForm(RepairerList.objects.get(user=77)))
        return context


class OrderCreate(CreateView):
    """" Adding a repair order """
    model = OrderList
    template_name = 'order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return JsonResponse({'message': f'<h3>Заявка № {self.object.pk} отправлена успешно!</h3>',
                             'num_order':self.object.pk,
                             'text_order': self.object.text_order,
                             'time_in': self.object.time_in,
                             'customer_name':self.object.customer_name,
                             'customer_phone': self.object.customer_phone,
                             'city': self.object.address_city,
                             'street': self.object.address_street_app,
                             'num': self.object.address_num,
                             })


    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.repairer_id = self.request.user
            form.instance.order_status = 'SND'
        return super(OrderCreate, self).form_valid(form)


class OrderManagementSystem(LoginRequiredMixin, ListView):
    """ list of all repair orders with Invoices"""

    model = OrderList
    context_object_name = 'order'
    template_name = 'order_list.html'

    def get_queryset(self):
        if self.request.GET.get('end'):
            self.queryset = OrderList.objects.filter(repairer_id=self.request.user)&\
                            OrderList.objects.filter(order_status='END')
        else:
            self.queryset = OrderList.objects.filter(repairer_id=self.request.user)&\
                            OrderList.objects.filter(order_status__in=['SND','RCV'])

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm
        return context


class OrderDatail(LoginRequiredMixin, DetailView):
    model = OrderList
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.queryset = OrderList.objects.filter(repairer_id=self.request.user)
        return self.queryset

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
    success_url = '/list_order'





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


class InvoiceCreate(DetailView):
    """ Create Invoice for payment """
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


        if self.object.order_status == 'SND':
            self.object.order_status = 'RCV'
            self.object.save()
        return context

    def post(self, formset, **kwargs):
        b = get_info1(self.kwargs.get('pk'))
        AuthorFormSet = modelformset_factory(Invoice, form=InvoiceForm)
        formset = AuthorFormSet(self.request.POST)
        instances = formset.save(commit=False)

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
           b.order_status = 'END'
           b.save()
        else:
            list_num = [{}]


        return JsonResponse(list_num, safe=False)



@require_http_methods(["GET"])
def DeleteIvoiceService(request, **kwargs):
    if request.user.is_authenticated:
        b = get_object_or_404(Invoice, pk=kwargs.get("invoice_pk"))
        b.delete()
        return JsonResponse({"message": "success"})



class Statistica(TemplateView):
    template_name = 'statistica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['a'] = OrderList.objects.values('time_in__month', 'time_in__year').annotate(sum=Sum(F('price'))).filter(repairer_id=self.request.user)
        # context['b'] = OrderList.objects.values('repairer_id__last_name').annotate(sum=Sum(F('price')),
        #                                                                            con=Count(F('id')))

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
        context['user_info'] = self.object.repairerlist
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.queryset = User.objects.filter(username=self.request.user)
        return self.queryset
