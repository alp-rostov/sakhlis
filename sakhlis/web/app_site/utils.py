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
from app_site.models import OrderList

GeoPointLocation = tuple[str, str]

def set_coordinates_address(street: str, city: str, house_number: str) -> GeoPointLocation | None:
    """ setting of map coordinates by street and city """
    try:
        geolocator = Nominatim(user_agent="app_site")
        location = geolocator.geocode({'city': city, 'street': street+', '+house_number}, addressdetails=True)
        if location:
            return str(location.longitude), str(location.latitude)
        else: return None
    except TypeError:
        return None

def get_telegram_button(repairer: list, order_pk: int) -> types.InlineKeyboardMarkup:
    """
    creating buttons for telegram message.
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
                 help_dict:dict = None,
                 name_graf:str = '',
                 name_legend:str = ''):

        self.name_graf=name_graf
        self.name_legend=name_legend
        self.queryset=queryset
        self.name_X=name_X
        self.data_Y=data_Y
        self.help_dict=help_dict     # help_dict is a WORK_CHOICES_ or MONTH_ or None
        self.fig, self.ax = plt.subplots()
    def get_data_for_graph(self) -> tuple[list, list]:

        labels = []
        data = []

        if self.help_dict:
            c = ''
            for _ in self.queryset:
                b = str(_.get('time_in__year')) if _.get('time_in__year') != c and _.get('time_in__year') else ' '
                labels.append(b + ' ' + self.help_dict[_[self.name_X]])
                data.append(_[self.data_Y])
                c = _.get('time_in__year')
        else:
            for _ in self.queryset:
                labels.append(_[self.name_X])
                data.append(_[self.data_Y])
        return labels, data

    def make_graf_pie(self):
        labels, data = self.get_data_for_graph()
        try:
            explode = [0.03, 0.01, 0.01, 0.01, 0.01]
            if len(labels) > 4:
                a = sum(data[5:len(data)])
                labels=labels[0:4]
                labels.append('Прочее')
                data=data[0:4]
                data.append(a)
            else:
                explode=explode[0:len(labels)]
            self.ax.pie(data, labels=labels, autopct='%1.1f%%',explode=explode)
            self.ax.set_title(self.name_graf)
            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()
        except Exception:
            self.fig = ''
        return self.sent(self.fig)

    def make_graf_bar(self):
        labels, data = self.get_data_for_graph()
        try:
            bar_labels = labels
            self.ax.bar(labels, data, label=bar_labels )
            self.ax.set_ylabel(self.name_legend)
            self.ax.set_title(self.name_graf)
            warnings.simplefilter("ignore", UserWarning)
            self.fig = plt.gcf()
        except Exception:
            self.fig =''
        return self.sent(self.fig)

    def make_graf_plot(self):
        labels, data = self.get_data_for_graph()
        try:
            bar_labels = labels
            self.ax.plot(labels, data, label=bar_labels)

            self.ax.set_ylabel(self.name_legend)
            self.ax.set_title(self.name_graf)

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


