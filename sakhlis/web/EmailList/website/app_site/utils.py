from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def sentmail(object, new):
    """ send a letter """
    html_content = render_to_string(
        'email.html',
        {
            'objectmail': object,
            'new': new
        }
    )

    msg = EmailMultiAlternatives(
        subject='TEST MAIL',
        from_email='alp-rostov@mail.ru',
        to=[object.email],
        headers={"Disposition-Notification-To": "alp-rostov@mail.ru"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
