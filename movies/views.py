from json.decoder import JSONDecodeError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Movie

import json
import requests

def index(request):
    movies=Movie.objects.all()
    return render(request,'index.html',{
        'movies':movies
    })

@csrf_exempt
def validateSeats(request):
    data=json.loads(request.body)
    movie=Movie.objects.get(title=data['movie_title'])
    all_booked_seats=movie.booked_seats.all()

    taken_seats=[]

    for i in data['seat_numbers']:
        if all_booked_seats.filter(seat_no=i):
            taken_seats.append(i)

    if taken_seats:
        return JsonResponse({
            'response':'sorry'
        })

    return JsonResponse({
        'response':'good'
    })


def makePayment(request):
    pass
    header={
        "Authorization": f"Bearer {YOUR_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data={
        "name": "Buttercup Brunch", 
        "amount": cost*100,
      "description": f"Payment for {no_of_seats} tickets for {movie_title}",
    }
    response=requests.post('https://api.paystack.co/page')
