from datetime import date
from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F, Prefetch, Count, Sum
from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from reportlab.lib import colors

from .models import RepairerList, OrderList, Invoice
from .filters import RepFilter, OrderFilter
from .forms import RepairerForm, BaseRegisterForm, OrderForm, InvoiceForm
from .utils import LetterMaker


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
        .select_related('repairer_id') \
        .prefetch_related(Prefetch('invoice_set', Invoice.objects
                                   .select_related('service_id')
                                   .defer('quantity_type', 'service_id__type')))\
                .defer('work_type', 'customer_name', 'customer_phone', 'customer_code', 'repairer_id__phone',
               'repairer_id__city', 'repairer_id__email', 'repairer_id__foto', 'repairer_id__active',
               'repairer_id__rating_sum', 'repairer_id__rating_num')

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
                                   .defer('quantity_type', 'service_id__type')
                                   .select_related('service_id').annotate(sum=F('price') * F('quantity'))))\
                                   .defer('work_type', 'customer_code', 'repairer_id__phone', 'repairer_id__city',
                                          'repairer_id__email', 'repairer_id__foto', 'repairer_id__active',
                                          'repairer_id__rating_sum', 'repairer_id__rating_num')


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
    order = Info.get_info(request.GET['pk_order']) #OrderList.objects.get(pk=request.GET['pk_order'])
    repaier = RepairerList.objects.get(pk=request.GET['pk_repairer'])
    if order and repaier:
        if not order.repairer_id:
            order.repairer_id = repaier
            order.save()
            return redirect(f'/list_order/{order.pk}')
        else:
            return redirect(f'/')  # TODO настроить сообщение, что ремонтник уже указан

class Info:
    def get_info(self, spk:int):
        return OrderList.objects.get(pk=spk)

class InvoiceCreate(Info, FormView):
    template_name = 'invoice.html'
    context_object_name = 'invoice'

    def get_form(self, form_class=None):
        InvoiceFormSet = modelformset_factory(Invoice, form=InvoiceForm, exclude=('order_id',))
        formset = InvoiceFormSet(queryset=Invoice.objects
                                 .filter(order_id=self.kwargs.get('order_pk'))
                                 .select_related('service_id')
                                 .defer('service_id__type'))

        return formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['info'] = self.get_info(self.kwargs.get('order_pk'))
        return context

    def post(self, formset, **kwargs):
        b=self.get_info(self.kwargs.get('order_pk'))
        AuthorFormSet = modelformset_factory(Invoice, fields='__all__')
        formset = AuthorFormSet(self.request.POST)
        instances = formset.save(commit=False)
        for instance in instances:
            instance.order_id = b
            instance.save()
        return redirect(f'/list_order/{self.kwargs.get("order_pk")}')

@require_http_methods(["GET"])
def DeleteIvoiceService(request, **kwargs):
    if request.user.is_authenticated:
        Invoice.objects.get(pk=kwargs.get("invoice_pk")).delete()
    return redirect(f'/invoice/{ kwargs.get("order_pk") }')


class Statistica(TemplateView):
    template_name = 'statistica.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # context['b']=OrderList.objects.all().exclude(time_out=None).order_by('-time_in').annotate(sum=Sum(F('invoice__price') * F('invoice__quantity')))
        context['a'] = OrderList.objects.values('time_in__date').annotate(sum=Sum(F('price')))
        context['b'] = OrderList.objects.values('repairer_id__name').annotate(sum=Sum(F('price')), con=Count(F('id')))

        return context

from django.http import FileResponse
import  io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Table as pdfTable
# from easy_pdf.rendering import render_to_pdf_response

@require_http_methods(["GET"])
def CreateIvoicePDF(request, **kwargs):
    # get information
    info=OrderList.objects \
        .annotate(sum=Sum(F('invoice__price') * F('invoice__quantity'))) \
        .prefetch_related(Prefetch('invoice_set', Invoice.objects
                                   .defer('quantity_type', 'service_id__type')
                                   .select_related('service_id').annotate(sum=F('price') * F('quantity')))) \
        .defer('work_type', 'customer_code', 'repairer_id__phone', 'repairer_id__city',
               'repairer_id__email', 'repairer_id__foto', 'repairer_id__active',
               'repairer_id__rating_sum', 'repairer_id__rating_num') \
        .get(pk=kwargs.get("order_pk"))

    # Create Bytestream buffer
    buf = io.BytesIO()
    # # Create a canvas
    # c = canvas.Canvas(buf, bottomup=0)
    #
    #
    # # Create a text object
    # textob = c.beginText()
    #
    # textob.setTextOrigin(inch, inch)
    #
    # textob.setFont("Helvetica", 25)
    #
    #
    # # Add some lines of text
    # date_info = str(info.time_in)[0:10:]
    # line = f'Invoice {info.pk}, date: {date_info}'
    #
    # textob.textLine(line)
    # c.drawText(textob)
    # # Create a table
    # table_data = [
    #               ['My Company: ', ' Gotsin S.A.', 'Customer company:', info.customer_name],
    #               ['Adress Company: ', ' Tbilisi, Zuraba Pataridze.', 'Customer Adress:', info.address_street_app],
    #               ['Code Company: ', ' 302265920', 'Customer code:', info.customer_code],
    #               ['Phone:', '+796044586678', 'Phone:', info.customer_phone],
    #               ['Bank:', 'Credo Bank'],
    #               ['CODE:', 'JSCRG22'],
    #               ['Account:', 'GE18CD0360000030597044']
    #               ]
    # table_data = table_data[::-1]
    # top_row = Table(table_data)
    #
    # top_row.setStyle(TableStyle([('ALIGN', (0, 0), (0, 6), 'RIGHT'),
    #                              ('ALIGN', (2, 0), (2, 6), 'RIGHT'),
    #                              ('FONT', (2, 0), (2, 6), 'Times-Bold'),
    #                              ('FONT', (0, 0), (0, 6), 'Times-Bold'),
    #                              ('SIZE',(0,0),(4,6),12)
    #                             ]
    #                             ))
    #
    # w, h = top_row.wrapOn(c, 0, 0)
    # top_row.drawOn(c, textob.getX()-10, textob.getY())
    # table_serv=[]
    # table_serv.append(['Name','Count','Price','Amount'])
    # for service in info.invoice_set.all():
    #     table_serv.append([service.service_id, service.quantity, service.price, service.sum])
    #
    # table_serv = table_serv[::-1]
    #
    #
    # top_row_serv = Table(table_serv)
    #
    # top_row_serv.setStyle(TableStyle([('FONT', (0, -1), (4, -1), 'Helvetica-Bold'),
    #                                   ('ALIGN', (0, -1), (4, -1), 'CENTER'),
    #                              ('SIZE', (0, -1), (4, -1), 15),
    #                                   ('LINEABOVE', (0, 0), (-1, -1), 2, colors.green),
    #                              ]
    #                             ))
    #
    # w, h = top_row_serv.wrapOn(c, 0, 0)
    # top_row_serv.drawOn(c, textob.getX()-35, textob.getY()+200)
    #



    # finish up


    # c.showPage()
    # c.save()

    doc = LetterMaker(buf, "The MVP", info)
    doc.createDocument()
    doc.savePDF()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'Invoice_{kwargs.get("order_pk")}_.pdf')





