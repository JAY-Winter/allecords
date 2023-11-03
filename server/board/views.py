from .models import Product
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
    query = request.GET.get('q')
    if query:
        product_objects = Product.objects.filter(name__icontains=query)
    else:
        product_objects = Product.objects.all()

    # 페이지네이션 구현 부분
    paginator = Paginator(product_objects, 9)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'board/product_table.html', {'products': products})
