from django.urls import path

from .views import index,validateSeats,webhook,occupiedSeats,makePayment,paymentConfirmed

app_name='movies'

urlpatterns = [
    path('',index,name='home'),
    path('check_seats/',validateSeats,name='check_seats'),
    path('occupied/',occupiedSeats,name='occupied'),
    path('webhook/',webhook,name='webhook'),
    path('payment/',makePayment,name='make_payment'),
    path('payment_confirmed/',paymentConfirmed,name='payment_confirmed'),
]

