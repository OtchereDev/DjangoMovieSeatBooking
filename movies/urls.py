from django.urls import path

from .views import index,validateSeats,webhook

app_name='movies'

urlpatterns = [
    path('',index,name='home'),
    path('check_seats/',validateSeats,name='check_seats'),
    path('webhook/',webhook,name='webhook'),
]

