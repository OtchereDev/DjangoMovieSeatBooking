from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

import hmac
import hashlib

def email_customer(first_name,email, seat_no, movie_title):
    # for formatting email to be sent
    rendered_msg = render_to_string('email_template.html', 
                                {'first_name': first_name,
                                'seat_no':seat_no,
                                'movie_title':movie_title})

    send_mail(
        'Thank you for Purchasing Us',
        rendered_msg,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def verify_webhook(request):
    secret=bytes(settings.PAYSTACK_SECRET,'utf-8')

    digester = hmac.new(secret, request.body, hashlib.sha512)
    calculated_signature = digester.hexdigest()

    if calculated_signature == request.META['HTTP_X_PAYSTACK_SIGNATURE']:
        return True
    else:
        False

