import json
import os

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.conf import settings

from basket.basket import Basket
from orders.views import payment_confirmation


@login_required
def BasketView(request):

    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    stripe.api_key = os.environ.get('STRIPE_API_KEY')

    # intent = stripe.PaymentIntent.create(
    #     amount = total,
    #     currency = 'gbp',
    #     metadata = {'userid' : request.user.id},
    #     description="Software development services",
    # )

    print('Execute Stripe Intent')
    intent = stripe.PaymentIntent.create(
        description="Software development services",
        shipping={
            "name": "Jenny Rosen",
            "address": {
                "line1": "510 Townsend St",
                "postal_code": "98140",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
            },
        },
        amount=total,
        currency="usd",
        payment_method_types=["card"],
    )

    context = {'client_secret': intent.client_secret}
    return render(request, 'payment/home.html', context)

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


# class Error(TemplateView):
#     template_name = 'payment/error.html' 


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    print('execute stripe_webhook')
    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)