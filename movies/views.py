
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from django.conf import settings

from .models import Movie,Payment,PaymentIntent,Seat
from .helpers import verify_webhook
from .tasks import mailing

import json
import requests

from ipware import get_client_ip


def index(request):
    movies=Movie.objects.all()
    return render(request,'index.html',{
        'movies':movies
    })


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
    data=json.loads(request.body)


    seat_numbers=list(map(lambda x: x+1 , data['seats_list']))
   
    movie_title=data['movie_title']
    cost=Movie.objects.get(title=movie_title).price
  
    header={
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET}",
        "Content-Type": "application/json"
    }
    data={
        "name": "Payment of Movie Ticket", 
        "amount": int((cost*len(seat_numbers)))*100,
        "description": f"Payment for {len(seat_numbers)} tickets for {movie_title}",
        "collect_phone": True,
        "redirect_url": f"{settings.HOST_URL}/payment_confirmed/"
        
    }
    
    response=requests.post('https://api.paystack.co/page',headers=header,json=data)

    if response.status_code==200:
        response_data=response.json()
        slug=response_data['data']['slug']
        redirect_url=f'https://paystack.com/pay/{slug}'
        PaymentIntent.objects.create(referrer=redirect_url,
                                    movie_title=movie_title,seat_numbers=seat_numbers)

        return JsonResponse({
            'payment_url':redirect_url
        })
    return JsonResponse({
        'error':'sorry service not available'
    })

@csrf_exempt
def webhook(request):
    if request.method=='POST':
        ip, is_routable = get_client_ip(request)

        if ip in settings.PAYSTACK_IP and verify_webhook(request):
            data=json.loads(request.body)
            if data['event']=='charge.success':
                first_name=data['data']['customer']['first_name']
                last_name=data['data']['customer']['last_name']
                email=data['data']['customer']['email']
                phone=data['data']['customer']['phone']
                amount=int(data['data']['amount'])/100

                referrer=data['data']['metadata']['referrer']
                payment_intent=PaymentIntent.objects.get(referrer=referrer)

                movie_title=payment_intent.movie_title
                movie=Movie.objects.get(title=movie_title)
                booked_seat=json.loads(payment_intent.seat_numbers)

                for seat_no in booked_seat:

                    seat=Seat.objects.create(seat_no=seat_no,
                    occupant_first_name=first_name,
                    occupant_last_name=last_name,
                    occupant_email=email)

                    movie.booked_seats.add(seat)
                    movie.save()

                    Payment.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            amount=amount/len(booked_seat),
                            phone=phone,
                            movie=movie,
                            seat_no=seat_no,)
                    
                    mailing.delay(first_name=first_name,email=email,
                                    seat_no=seat_no,movie_title=movie_title)

            return HttpResponse(200)
    return HttpResponseForbidden()


def occupiedSeats(request):
    
    data=json.loads(request.body)
    movie=Movie.objects.get(title=data['movie_title'])

    occupied=movie.booked_seats.all()
    occupied_seat=map(lambda x : x.seat_no - 1,occupied)

    return JsonResponse({
        'occupied_seat':list(occupied_seat),
        'movie':str(movie)
    })

def paymentConfirmed(request):
    # return render(request,'payment_confirmed.html')
    return HttpResponse('<h2>Thank you for purchasing Us....</h2>\n\
        <h2>An email has been sent to your email address with your seat number</h2>\n\
        <h2>Thank you once again</h2>\n\
        <a href="/" >Click here to go to homepage</a>',)