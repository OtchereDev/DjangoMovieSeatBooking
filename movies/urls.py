from django.urls import path

from .views import index,validateSeats

app_name='movies'

urlpatterns = [
    path('',index,name='home'),
    path('check_seats/',validateSeats,name='check_seats'),
]

