from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.core.paginator import (Paginator,
                                   PageNotAnInteger,
                                   EmptyPage)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


def category(request):
    all_category = Category.objects.all()
    pagination = get_paginated_objects(request, all_category, 5)
    return render(request,
                  'shop/categories.html',
                  {'pagination': pagination})


def products(request):
    all_product = Product.objects.all()
    pagination = get_paginated_objects(request, all_product, 5)
    return render(request,
                  'shop/products.html',
                  {'pagination': pagination})


def subcategory(request, category_slug):
    all_subcategory = Subcategory.objects.filter(category__slug=category_slug).all()
    pagination = get_paginated_objects(request, all_subcategory, 5)
    return render(request,
                  'shop/subcategory.html',
                  {'pagination': pagination})


def get_paginated_objects(request, objects, num_per_page):
    paginator = Paginator(objects, num_per_page)
    page = request.GET.get('page', 1)
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)
    return paginated_objects


@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id, quantity):
    cart = Cart.objects.get_object_or_404(user=request.user)
    product = Product.objects.get(pk=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.quantity += quantity
    cart_item.save()
    return JsonResponse({"message": "Product added to cart successfully"})


@permission_classes([IsAuthenticated])
def update_cart_item(request, cart_item_id, new_quantity):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.quantity = new_quantity
    cart_item.save()
    return JsonResponse({"message": "Cart item quantity updated successfully"})


@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return JsonResponse({"message": "Product removed from cart successfully"})


@permission_classes([IsAuthenticated])
def cart_sum():
    cart_item = CartItem.objects.all()
    sum_price = 0
    count = 0
    for item in cart_item:
        sum_price += item.product.price * item.quantity
        count += item.quantity
    return sum_price, count


@permission_classes([IsAuthenticated])
def cart_clear(request):
    cart = Cart.objects.get_object_or_404(user=request.user)
    cart.items.clear()
    return JsonResponse({"message": "Cart cleared successfully"})