import django.http
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse

from .db_utils import get_todays_collection

PRODUCTS_PER_PAGE = 16


def product_list(request):
    todays_collection = get_todays_collection()
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    page = request.GET.get('page', 1)  # 현재 페이지 번호를 기본값으로 설정

    # MongoDB 쿼리셋을 구성합니다. 이름으로 필터링할 수 있습니다.
    if query:
        product_objects = todays_collection.find({'name': {'$regex': query, '$options': 'i'}})
    else:
        product_objects = todays_collection.find()

    # 정렬 파라미터가 있으면 정렬 방향을 결정하고 적용합니다.
    if sort == 'price_asc':
        product_objects = product_objects.sort('price', 1)
    elif sort == 'price_desc':
        product_objects = product_objects.sort('price', -1)

    # 쿼리셋을 리스트로 변환합니다.
    product_list = list(product_objects)
    paginator = Paginator(product_list, PRODUCTS_PER_PAGE)

    try:
        # 사용자가 요청한 페이지 번호에 해당하는 상품 페이지를 가져옵니다.
        products = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우 첫 페이지로 리다이렉트합니다.
        return django.http.HttpResponseRedirect(reverse('product_list') + '?q={}&sort={}'.format(query, sort))
    except EmptyPage:
        # 페이지 번호가 범위를 벗어난 경우 마지막 페이지로 리다이렉트합니다.
        return django.http.HttpResponseRedirect(
            reverse('product_list') + '?q={}&sort={}&page={}'.format(query, sort, paginator.num_pages))

    # 렌더링할 템플릿과 함께 컨텍스트를 전달합니다.
    return render(request, 'board/product_table.html', {
        'products': products,
        'query': query,
        'sort': sort,
        'page': page
    })


def recommend_melon_product_list(request):
    todays_collection = get_todays_collection()

    # 각 아티스트를 순회하면서 컬렉션 내에 존재하는지 확인하고 제품 정보를 수집
    products = []

    artists = []
    # 각 차트 엔트리를 JSON 형식으로 변환하고 출력합니다.
    chart = ChartData(fetch=True)
    for index in range(len(chart)):
        chart_entry_json = chart[index].json()
        artist = json.loads(chart_entry_json)['artist']
        artists.append(artist)

    for artist in artists:
        cursor = todays_collection.find({"artist": {"$regex": artist, "$options": "i"}})
        for document in cursor:
            # '_id'를 문자열로 변환하여 JSON 직렬화 가능하도록 함
            document['_id'] = str(document['_id'])
            products.append(document)

    return render(request, 'board/recommend_melon_product_list.html', {'products': products})
