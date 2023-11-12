
from django.db.models import F, Prefetch, Sum, Count
from geopy.geocoders import Nominatim
from telebot import types
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
import matplotlib.pyplot as plt
import matplotlib

import base64
import urllib.parse
import warnings
import io

from .models import OrderList, Invoice

def get_info_for_pdf():
    return OrderList.objects \
        .annotate(sum=Sum(F('invoice__price') * F('invoice__quantity'))) \
        .prefetch_related(Prefetch('invoice_set', Invoice.objects
                                   .defer('quantity_type', 'service_id__type')
                                   .select_related('service_id')
                                   .annotate(sum=F('price') * F('quantity')))
                          ).select_related('repairer_id')

def get_data_for_graph(queryset, labels_name:str, data_name:str, help_dict:dict=None) -> tuple:
    """ return dicts using for create Graph in statistica.html """
    labels = []
    data = []
    if help_dict:
        for _ in queryset:
            labels.append(help_dict[_[labels_name]])
            data.append(_[data_name])
    else:
        for _ in queryset:
            labels.append(_[labels_name])
            data.append(_[data_name])

    return labels, data

def set_coordinates_address(street: str, city: str, app_num: str) -> str:
    """ setting of map coordinates by street and city """
    try:
        geolocator = Nominatim(user_agent="app_site")
        location = geolocator.geocode(street + ', ' + app_num + ', ' + city)
    except TypeError:
        return ' '
    if location:
        return f'https://yandex.ru/maps/?pt={location.longitude},{location.latitude}&z=18&l=map'

def add_telegram_button(repairer: list, order_pk: int) -> types.InlineKeyboardMarkup:
    """
    creating buttons for telegram message.
    repairer -> list of tuples (id repairer, s_name repairer)
    order_pk -> order`s number
    """
    keyboard = types.InlineKeyboardMarkup()
    button = []
    for i in repairer:
        url_ = f'http://127.0.0.1:8000/add?pk_order=' \
               f'{order_pk}&pk_repairer={i[0]}'
        button.append(types.InlineKeyboardButton(text=i[1], url=url_))
    return keyboard.add(*button)

class InvoiceMaker(object):
    """ create pdf-invoice """
    def __init__(self, pdf_file, info):
        self.c = canvas.Canvas(pdf_file, bottomup=0)
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        self.info = info

    def createDocument(self) -> None:
        # create an invoice’s header
        date_info = str(self.info.time_in)[0:10:]
        line = f'Invoice  {self.info.pk}, date: {date_info}'

        self.createParagraph(line, *self.coord(60, 30), style='Heading1')

        # create a table containing information about companies
        data = [
            ['My Company: ', ' Gotsin S.A.', 'Customer company:', self.info.customer_name],
            ['Adress Company: ', ' Tbilisi, Zuraba Pataridze.', 'Customer Adress:', self.info.address_street_app + ', ' + self.info.address_num],
            ['Code Company: ', ' 302265920', 'Customer code:', self.info.customer_code],
            ['Phone:', '+995598259119', 'Phone:', self.info.customer_phone],
            ['Bank:', 'Credo Bank'],
            ['CODE:', 'JSCRG22'],
            ['Account:', 'GE18CD0360000030597044']
        ]
        data = data[::-1]

        a = TableStyle([('ALIGN', (0, 0), (0, 6), 'RIGHT'),
                        ('ALIGN', (2, 0), (2, 6), 'RIGHT'),
                        ('FONT', (2, 0), (2, 6), 'Times-Bold'),
                        ('FONT', (0, 0), (0, 6), 'Times-Bold'),
                        ('SIZE', (0, 0), (4, 6), 10)
                        ]
                       )

        self.createTable(data, 30, 120, a, 1.8 * inch)

        # create a table list of services
        table_serv = []
        table_serv.append(['Name', 'Count', 'Price', 'Amount'])
        i = 1
        sum_ = 0
        for service in self.info.invoice_set.all():
            table_serv.append([service.service_id, service.quantity, service.price, round(service.sum, 2)])
            i = i + 1
            sum_ = sum_ + service.sum
        table_serv.append(['', '', 'Total:', round(sum_, 2)])

        table_serv = table_serv[::-1]
        c_width = [200, 80, 80, 80]
        b = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('FONT', (0, -1), (4, -1), 'Helvetica-Bold'),
            ('SIZE', (0, -1), (4, -1), 12),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('SIZE', (2, 0), (3, 0), 12),
        ]
        )

        self.createTable(table_serv, 70, 280, b, c_width)

        self.createParagraph('Sign_____________S.A.Gostin', *self.coord(50, 110 + i * 10), style='Heading4')

    def coord(self, x, y, unit=1) -> tuple:
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, y * unit
        return x, y

    def createParagraph(self, ptext, x, y, style=None):
        """"""
        if not style:
            style = self.styles["Normal"]
        else:
            style = self.styles[style]
        p = Paragraph(ptext, style=style)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))

    def createTable(self, data, x, y, TableStyle_, c_width):
        """"""
        table = Table(data, colWidths=c_width)
        table.setStyle(TableStyle_)
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(x, y))

    def savePDF(self):
        """"""
        self.c.showPage()
        self.c.save()



class Graph:
    """ create a graph and sent to template """
    def __init__(self, labels:dict, data:dict, name_graf:str, name_legend:str):
        self.labels=labels
        self.data=data
        self.name_graf=name_graf
        self.name_legend=name_legend
        self.fig, self.ax = plt.subplots()

    def make_graf_pie(self):
        try:
            explode = [0.03, 0.01, 0.01, 0.01, 0.01]
            if len(self.labels) > 4:
                a = sum(self.data[5:len(self.data)])
                self.labels=self.labels[0:4]
                self.labels.append('Прочее')
                self.data=self.data[0:4]
                self.data.append(a)
            else:
                explode=explode[0:len(self.labels)]
            self.ax.pie(self.data, labels=self.labels, autopct='%1.1f%%',explode=explode)
            self.ax.set_title(self.name_graf)
            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()
        except Exception:
            self.fig = ''
        return self.sent(self.fig)

    def make_graf_bar(self):
        try:
            bar_labels = self.labels
            self.ax.bar(self.labels, self.data, label=bar_labels )
            self.ax.set_ylabel(self.name_legend)
            self.ax.set_title(self.name_graf)
            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()
        except Exception:
            self.fig =''
        return self.sent(self.fig)

    def make_graf_plot(self):
        try:
            bar_labels = self.labels
            self.ax.plot(self.labels, self.data, label=bar_labels)

            self.ax.set_ylabel(self.name_legend)
            self.ax.set_title(self.name_graf)

            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()

        except Exception:
            self.fig=''

        return self.sent(self.fig)


    def sent(self, fig):
        if self.fig!='':
            buf=io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            return urllib.parse.quote(string)
        else:
            pass


# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.
#
#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         print(request.GET)
#         print(request.POST)
#         print('---------------')
#         response = self.get_response(request)
#         print(request.GET)
#         print(request.POST)
#         print('++++++++++++++++')
#         # Code to be executed for each request/response after
#         # the view is called.
#
#         return response


