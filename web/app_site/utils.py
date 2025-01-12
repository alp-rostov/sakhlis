import _io
import os
from uuid import UUID

import qrcode
import reportlab
from geopy.geocoders import Nominatim
from reportlab.lib import styles
from PIL import Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from telebot import types
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
import matplotlib.pyplot as plt
import base64
import urllib.parse
import warnings
import io

from .constants import CITY_CHOICES_INVOICE
from .models import OrderList


class Location:
    """ to get geopoint using address and save to model"""
    def __init__(self, instance: OrderList):
        self.instance = instance

    def set_location(self):
        geolocator = Nominatim(user_agent="app_site")
        location = geolocator.geocode({'city': 'Тбилиси',
                                       'street': str(self.instance.address_street_app) + ', ' + str(
                                           self.instance.address_num)},
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
        if self.instance.location_longitude is not None:
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


class CreatePDF(object):
    """ create pdf-document -> the invoice for payment """

    def __init__(self, pdf_file: _io.BytesIO, info_order: OrderList=None):
        """ pdf_file = io.BytesIO()"""
        self.c = canvas.Canvas(pdf_file, bottomup=0)
        folder = os.path.dirname(reportlab.__file__)
        folder_font = os.path.join(folder, 'fonts')

        custom_font = os.path.join(folder_font, 'Tantular.ttf') # add file to ...reportlab/fonts
        gergian_font = os.path.join(folder_font, 'ARIALUNI.TTF')
        lary_font = os.path.join(folder_font, 'font-larisome.ttf')
        pdfmetrics.registerFont(TTFont('Tantular', custom_font,))
        pdfmetrics.registerFont(TTFont('Georgian', gergian_font, ))
        pdfmetrics.registerFont(TTFont('font-larisome', lary_font, ))
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Top_Right',
                                  fontName='Georgian',
                                  bulletAnchor='start',
                                  alignment=TA_RIGHT,
                                  fontSize=14,
                                  leading=22,
                                  # textColor=colors.black,
                                  borderPadding=0,
                                  leftIndent=0,
                                  rightIndent=0,
                                  spaceAfter=0,
                                  spaceBefore=0,
                                  spaceShrinkage=0.05,
                                  ))
        self.styles.add(ParagraphStyle(name='Invoice_center',
                                       fontName='Helvetica',
                                       fontSize=25,
                                       leading=13,
                                       leftIndent=70,
                                       rightIndent=70,
                                       spaceBefore=0,
                                       spaceAfter=0,
                                       backColor='#efefef',
                                       borderWidth=1,
                                       borderPadding=20,
                                       borderColor='#8c8a8a',
                                       borderRadius=5,
                                       ))


        self.width, self.height = A4
        self.info_order = info_order

    def createDocument_invoice(self) -> None:
        # create a header
        date_info = str(self.info_order.time_in)[0:10]
        #
        line1 = ('ინდივიდუალურიმეწარმე სერგეი გოცინ <br />'
                 'საქართველო, თბილისი, დიდუბის რაიონი, <br />'
                 'მურმან ლებანიძის ქუჩა, N 10, <br />'
                 'სართული 1, ბინა N3 <br />'
                 'საიდენტიფიკაციო ნომერი: 302264920 <br />'
                 'კრედო ბანკი <br /> ბანკის კოდი JSCRG22 <br /> '
                 'ა/ა GE18CD0360000030597044<br />')

        self.createParagraph(line1, *self.coord(-20, -45), style='Top_Right')

        line2 = f'<b>Invoice # {self.info_order.pk} </b><br /><br /><font fontsize=18>Data {date_info}</font>'
        self.createParagraph(line2, *self.coord(0, 80), style='Invoice_center')

        line3 = (f'<font fontName="Georgian">Invoiced To: <br /><b>{self.info_order.customer_id.customer_name}</b><br />'
                 f'{self.info_order.apartment_id}, {CITY_CHOICES_INVOICE[self.info_order.apartment_id.address_city]}</font>')

        self.createParagraph(line3, *self.coord(20, 95), style='Heading2')

        #create a service list
        table_serv = []
        table_serv.append(['#', 'მომსახურება/პროდუქტები', 'რაოდენობა', 'ფასი', 'ჯამი']) # name / count/price/amount
        i = 1
        sum_ = 0
        for service in self.info_order.invoice_set.all():
            table_serv.append([i,service.service_id, service.quantity, service.price, round(service.sum, 2)])
            i = i + 1
            sum_ = sum_ + service.sum
        table_serv.append(['','', '', '', f'{round(sum_, 2)} e'])

        table_serv = table_serv[::-1]
        c_width = [20, 220, 80, 80, 80]
        b = TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('TEXTCOLOR', (0, -1), (5, -1), '#FFFFFF'),
            ('FONTSIZE', (0, -1), (5, -1), 12),
            ('FONTNAME', (0, 0), (-1, -1), 'Georgian'),
            ('BACKGROUND', (0, -1), (5, -1), '#666666'),
            ('GRID', (0, -1), (5, -1), 1.5, '#FFFFFF'),
            ('LINEBELOW', (0, 0), (5, -3), 0.5, '#666666'),
            ('FONTSIZE', (0, 0), (5, 0), 12),
            ('BOX', (4, 0), (5, 0), 0.5, '#666666'),
            ('FONTNAME', (4, 0), (5, 0), 'font-larisome'),
            ('ALIGN', (2, 0), (5, -1), 'CENTER')
        ]
        )
        self.createTable(table_serv, 50, 360, b, c_width)

        self.createParagraph('<font fontName="Georgian">ინდივიდუალური მეწარმე      '
                             '<img src="static/images/sign.png" valign="top" width=70 height=55 />'
                             '      სერგეი გოცინ</font>',
                             *self.coord(50, 160+i * 10), style='Heading3')

        line4 = (f'<b>Repair service in Tbilisi </b><br />'
                 f'+995 598 259 119 | '
                 f'<a href="https://www.sakhlis-remonti.ge/" color="blue">www.sakhlis-remonti.ge</a> |'
                 f'alprostov.1982@gmail.com')
        self.createParagraph(line4, *self.coord(20, 270), style='Normal')
        # self.createQRcode( 400, 580, 70, 'https://www.sakhlis-remonti.ge/' )

    def coord(self, x, y, unit=1) -> tuple:
        """ Helper class to help position flowables in Canvas objects """
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

    # def createQRcode(self, x, y, width:int=None, str_:str=''):
    #     _ = create_qr_code_url(f'{str_}')
    #     with Image.open(_) as Im:
    #         ir = ImageReader(Im)
    #         self.c.drawImage(ir, *self.coord(x, y), width, preserveAspectRatio=True, mask='auto')

    def savePDF(self):
        self.c.showPage()
        self.c.save()


class Graph:
    """ create a graph"""
    def __init__(self,
                 queryset,
                 name_X: str,
                 data_Y: str,
                 help_dict: dict = None,  # help_dict is a WORK_CHOICES_ or MONTH_ or None
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
                explode = explode[0:len(self.labels)]
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
            self.fig = ''

        return self.sent(self.fig)

    def sent(self, fig):
        if self.fig != '':
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            return urllib.parse.quote(string)


def is_valid_uuid(uuid_to_test, version=4):
    """    Check if uuid_to_test is a valid UUID.    """
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    except TypeError:
        return False
    return True


def coding_personal_data(**kwargs):
    ''' coding contact information showing without authentication '''
    def code_data(code: str or None) -> str:
        if not code:
            return ''
        if len(code) >= 7:
            return f'{code[0:-5]}**{code[-3:-1]}*'
        elif 5 <= len(code) < 7:
            return f'{code[0:-2]}**'
        elif len(code) < 5:
            return f'{code[0:-1]}*'
    return dict(map(lambda  x: (x[0], code_data(x[1])) , kwargs.items()))

def create_qr_code_url(url:str):
    ''' Generate the QR code image and save to buffer'''
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=12, border=1,  )
    qr.add_data(url)
    qr.make()
    img_ = qr.make_image(fill_color="#FF8000", back_color="white")
    return img_


def get_qrcode_for_client():
    pass




