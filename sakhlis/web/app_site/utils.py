from geopy.geocoders import Nominatim
from telebot import types
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle



def set_coordinates_address(street: str, city: str) -> str:
    """ setting of coordinates by street and city """
    try:
        geolocator = Nominatim(user_agent="app_site", )
        location = geolocator.geocode({'street': {street}, 'city': {city}}, addressdetails=True)
    except TypeError:
        return ' '
    else:
        if location:
            return f'https://yandex.ru/maps/?pt={location.longitude},{location.latitude}&z=18&l=map'
        else:
            return ' '

########################################################################

def add_telegram_button(repairer: list, order_pk: int):
    """
    creating buttons for telegram message.
    repairer -> list of tuples (id repairer, s_name repairer)
    order_pk -> order`s number
    """
    # создание кнопок в телеграмм
    keyboard = types.InlineKeyboardMarkup()
    button = []
    for i in repairer:
        url_ = f'http://127.0.0.1:8000/add?pk_order=' \
               f'{order_pk}&pk_repairer={i[0]}'
        button.append(types.InlineKeyboardButton(text=i[1], url=url_))
    return keyboard.add(*button)


########################################################################


class InvoiceMaker(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, pdf_file, info):
        self.c = canvas.Canvas(pdf_file, bottomup=0)
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        self.info = info

    # ----------------------------------------------------------------------
    def createDocument(self):
        """"""
        # create an invoice’s header
        date_info = str(self.info.time_in)[0:10:]
        line = f'Invoice  {self.info.pk}, date: {date_info}'

        self.createParagraph(line, *self.coord(60, 30), style='Heading1')

        # create a table containing information about companies
        data = [
            ['My Company: ', ' Gotsin S.A.', 'Customer company:', self.info.customer_name],
            ['Adress Company: ', ' Tbilisi, Zuraba Pataridze.', 'Customer Adress:', self.info.address_street_app],
            ['Code Company: ', ' 302265920', 'Customer code:', self.info.customer_code],
            ['Phone:', '+796044586678', 'Phone:', self.info.customer_phone],
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

    # ----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, y * unit
        return x, y

        # ----------------------------------------------------------------------

    def createParagraph(self, ptext, x, y, style=None):
        """"""
        if not style:
            style = self.styles["Normal"]
        else:
            style = self.styles[style]
        p = Paragraph(ptext, style=style)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))

    # ----------------------------------------------------------------------

    def createTable(self, data, x, y, TableStyle_, c_width):
        """"""
        table = Table(data, colWidths=c_width)
        table.setStyle(TableStyle_)
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(x, y))

    # ---------------------------------------------

    def savePDF(self):
        """"""
        self.c.showPage()
        self.c.save()

    # ----------------------------------------------------------------------

def order_status():
    status = ['Заказ получен', 'Направлен мастеру', 'Выполнен', 'Отменен']


    return status