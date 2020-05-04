from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from ec.models import Product



'''
@require_POST
def cart_add(request, product_id):
    if not Product.objects.filter(id=product_id).exists():
        raise Http404
    cart = request.session.get('cart')
    if cart:
        cart.append(product_id)
        request.session['cart'] = cart
    else:
        request.session['cart'] = [product_id]
    return redirect('/')

{'cart': []}








@require_POST
def cart_remove(request, product_id):
'''
def cart_add(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect(request.META['HTTP_REFERER'])


def cart_add_2(request, product_id, amount):
    cart = request.session.get('cart', {})
    cart['product_id'] += amount
    request.session['cart'] = cart
    return redirect(request.META['HTTP_REFERER'])


'''
class CartAdd(generic.ListView):
    
    template_name = 'ec/product_detail.html'
    model = Post
    
    def post(sefl, request, *args, **kwargs):
        value = request.POST.getlist('')
'''