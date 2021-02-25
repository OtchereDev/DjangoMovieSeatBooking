from celery import shared_task
from movieWebsite.celery import app
from .helpers import email_customer


@shared_task
def add(x, y):
    return x + y

@app.task(name='email customer')
def mailing(first_name, email, seat_no, movie_title):
    email_customer(first_name=first_name,email=email,
                            seat_no=seat_no,movie_title=movie_title)

                            