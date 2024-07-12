PERMISSION_FOR_REPAIER = 'app_site.view_invoice'
PERMISSION_FOR_OWNER = 'app_site.view_orderlist'


APART_CHOICES = [
    ('FL', 'Flat'),
    ('HM', 'Home'),
    ('OF', 'Office'),
    ('RS', 'Restaurant'),
    ('SH', 'Store'),
    ('OT', 'Other'),
]


CITY_CHOICES = [
    ('TB', 'Tbilisi'),
    ('BT', 'Batumi'),
    ('GD', 'Gudaury'),

]

WORK_CHOICES = [
    ('EL', 'Electrician'),
    ('PL', 'Plumbing'),
    ('SP', 'Conditioning'),
    ('FT', 'Furniture repair/installation'),
    ('OT', 'Repair of windows and doors'),
    ('ID', 'Installation of equipment'),
    ('BL', 'Construction works'),
    ('CL', 'Cleaning'),

]

WORK_CHOICES_ = {
    'EL': 'Electrician',
    'PL': 'Plumbing',
    'SP': 'Conditioning',
    'FT': 'Furniture repair/installation',
    'OT': 'Repair of windows and doors',
    'ID': 'Installation of equipment',
    'BL': 'Construction works',
    'CL': 'Cleaning'
}


QUANTITY_CHOICES = [
    ('SV', 'Service'),
    ('ME', 'Meter'),
    ('QL', 'Kilogram'),
    ('TH', 'Thing'),

]

ORDER_STATUS = [
    # ('BEG', 'Request received'),
    ('SND', 'New requests'),
    ('RCV', 'Request sent to the master'),
    ('END', 'Request finished'),
]

orderstat=['SND', 'RCV', 'END']

ORDER_STATUS_ = [
    # ('BEG', 'New requests'),
    ('SND', 'New job'),
    ('RCV', 'Job in progress'),
    ('END', 'Job completed '),
]



ORDER_STATUS_FOR_CHECK = ['SND', 'RCV', 'WRK', 'END']


MONTH = [
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),

]


MONTH_ = ['','Jan', 'Feb', 'Mch', 'Aprl', 'May',
    'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
    'Nov', 'Dec']

