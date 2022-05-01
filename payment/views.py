from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from basket.basket import Basket
import os

import stripe

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