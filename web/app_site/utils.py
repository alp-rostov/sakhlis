import _io

from geopy.geocoders import Nominatim
from telebot import types
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
import matplotlib.pyplot as plt
import base64
import urllib.parse
import warnings
import io

from .models import OrderList

ww=22
class Location:
    def __init__(self, instance: OrderList):
        self.instance = instance

    def set_location(self):
        geolocator = Nominatim(user_agent="app_site")
        location = geolocator.geocode({'city': 'Тбилиси',
                                   'street': str(self.instance.address_street_app)+', '+str(self.instance.address_num)},
                                    addressdetails=True)
        if location:
            return str(location.longitude), str(location.latitude)
        return None

    def save_location(self):
        try:
            longitude, latitude = self.set_location()
            self.instance.location_longitude = float(longitude)
            self.instance.location_latitude = float(latitude)
            self.instance.save()
        except (TypeError, AttributeError):
            return None

    def print_yandex_location(self):
        if self.instance.location_longitude != None:
            return f'https://yandex.ru/maps/?pt={self.instance.location_longitude},{self.instance.location_latitude}&z=18&l=map'
        return ' '



def get_telegram_button(repairer: list, order_pk: int) -> types.InlineKeyboardMarkup:
    """
    creating buttons for telegram-bot message.
    repairer -> list of tuples [(id repairer, s_name repairer),....]
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
    """ create pdf-document -> an invoice for payment """
    def __init__(self, pdf_file: _io.BytesIO, info: OrderList):
        """ pdf_file = io.BytesIO()"""
        self.c = canvas.Canvas(pdf_file, bottomup=0)
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        self.info = info

    def createDocument(self) -> None:
        # create a header
        date_info = str(self.info.time_in)[0:10]
        line = f'Invoice № {self.info.pk}, date: {date_info}'

        self.createParagraph(line, *self.coord(60, 30), style='Heading1')

        # create a table containing company information
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

        # create a service list
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
        if not style:
            style = self.styles["Normal"]
        else:
            style = self.styles[style]
        p = Paragraph(ptext, style=style)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))

    def createTable(self, data, x, y, TableStyle_, c_width):
        table = Table(data, colWidths=c_width)
        table.setStyle(TableStyle_)
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(x, y))

    def savePDF(self):
        self.c.showPage()
        self.c.save()


class Graph:
    """ create a graph"""
    def __init__(self,
                 queryset,
                 name_X: str,
                 data_Y: str,
                 help_dict: dict = None,          # help_dict is a WORK_CHOICES_ or MONTH_ or None
                 name_graf: str = '',
                 name_legend: str = ''):

        self.name_X = name_X
        self.data_Y = data_Y
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylabel(name_legend)
        self.ax.set_title(name_graf)

        def get_data_for_graph(queryset) -> tuple[list, list]:
            labels = []
            data = []
            if help_dict:
                c = ''
                for _ in queryset:
                    b = str(_.get('time_in__year') or '')
                    labels.append(b + ' ' + help_dict[_[self.name_X]])
                    data.append(_[self.data_Y])
                    c = _.get('time_in__year')
            else:
                for _ in queryset:
                    labels.append(_[self.name_X])
                    data.append(_[self.data_Y])


            return labels, data

        self.labels, self.data = get_data_for_graph(queryset)

    def make_graf_pie(self):
        try:
            explode = [0.03, 0.01, 0.01, 0.01, 0.01]
            if len(self.labels) > 4:
                a = sum(self.data[5:len(self.data)])
                self.labels = self.labels[0:4]
                self.labels.append('Other')
                self.data = self.data[0:4]
                self.data.append(a)
            else:
                explode=explode[0:len(self.labels)]
            self.ax.pie(self.data, labels=self.labels, autopct='%1.1f%%', explode=explode)

            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()
        except Exception:
            self.fig = ''
        return self.sent(self.fig)

    def make_graf_bar(self):
        try:
            self.ax.bar(self.labels, self.data, label=self.labels)
            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()
        except Exception:
            self.fig = ''
        return self.sent(self.fig)

    def make_graf_plot(self):
        try:
            self.ax.plot(self.labels, self.data, label=self.labels)
            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()

        except Exception:
            self.fig=''

        return self.sent(self.fig)

    def sent(self, fig):
        if self.fig != '':
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            return urllib.parse.quote(string)


