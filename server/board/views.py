from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .db_utils import get_todays_collection

PRODUCTS_PER_PAGE = 16  # 페이지 당 상품 수를 상수로 정의


def product_list(request):
    todays_collection = get_todays_collection()

    query = request.GET.get('q')
    if query:
        product_objects = todays_collection.find({'name': {'$regex': query, '$options': 'i'}})
    else:
        product_objects = todays_collection.find()

    product_list = list(product_objects)
    paginator = Paginator(product_list, PRODUCTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'board/product_table.html', {'products': products})