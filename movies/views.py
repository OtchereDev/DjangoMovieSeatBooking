from json.decoder import JSONDecodeError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.conf import settings

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

    for i in data['seats_list']:
        if all_booked_seats.filter(seat_no=i):
            taken_seats.append(i)

    if taken_seats:
        return JsonResponse({
            'response':'sorry',
            'taken_seats':taken_seats
        })

    return JsonResponse({
        'response':'good'
    })


def makePayment(request):
    data=json.loads(requests.body)

    seat_numbers=data['seats_list']
    movie_title=data['movie_title']
    cost=Movie.objects.get(title=movie_title).price
  
    header={
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET}",
        "Content-Type": "application/json"
    }
    data={
        "name": "Payment of Movie Ticket", 
        "amount": int(cost)*100,
        "description": f"Payment for {len(seat_numbers)} tickets for {movie_title}",
        'collect_phone': True,
        "metadata":{
            "seats_numbers":seat_numbers,
            "movie_title":movie_title
        }
    }
    
    response=requests.post('https://api.paystack.co/page',headers=header,json=data)

    if response.status_code=='200':
        response_data=response.json()
        slug=response_data['data']['slug']
        redirect_url=f'https://paystack.com/pay/{slug}'

        return JsonResponse({
            'payment_url':redirect_url
        })

    # for formatting email to be sent
    rendered = render_to_string('email_template.html', {'foo': 'bar'})



@csrf_exempt
def webhook(request):
    data=json.loads(request.body)
    print(data)
    return HttpResponse(200)
