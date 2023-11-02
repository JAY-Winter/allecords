from .models import Product
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
    product_objects = Product.objects.all()
    paginator = Paginator(product_objects, 10)  # 한 페이지 당 10개의 제품

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # 페이지가 정수가 아닐 때, 첫 번째 페이지 반환
        products = paginator.page(1)
    except EmptyPage:
        # 페이지 범위를 벗어났을 때, 마지막 페이지 반환
        products = paginator.page(paginator.num_pages)

    return render(request, 'board/product_table.html', {'products': products})
