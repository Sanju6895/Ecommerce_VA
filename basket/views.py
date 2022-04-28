from django.shortcuts import render
from .basket import Basket
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
#from django.contrib.sessions.models import Session

# Create your views here.
def basket_summary(request):
    basket = Basket(request)
    context= {'basket': basket}
    return render(request, 'basket/summary.html', context)


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

# def basket_add(request):
#     basket = Basket(request)
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('productid'))
#         product_qty = int(request.POST.get('productqty'))

#         product = get_object_or_404(Product, id=product_id)
#         basket.add(product=product, product_qty =product_qty)
#         response = JsonResponse({'qty':'product_qty'})
#         return response