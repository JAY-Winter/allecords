from django.shortcuts import render
from .models import Product


def show_products(request):
    products = Product.objects.all()
    return render(request, 'board/product_table.html', {'products': products})
