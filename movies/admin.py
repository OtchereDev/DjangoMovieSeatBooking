from django.contrib import admin
from .models import Movie,Seat,Payment,PaymentIntent

admin.site.register(Movie)
admin.site.register(Seat)
admin.site.register(Payment)
admin.site.register(PaymentIntent)
