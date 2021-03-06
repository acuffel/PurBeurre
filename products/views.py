import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Product, Substitute

logger = logging.getLogger(__name__)


def search(request):
    """
    :param request: User's input
    :return: List of products
    """
    search_products = request.POST.get('search_products').lower()
    products_db = Product.objects.filter(product_name__istartswith=
                                         search_products).values()
    context = {
        'products': products_db,
        'search_products': search_products
    }
    logger.info('New search', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })
    return render(request, 'products/aliments.html', context)


def detail(request, product_id):
    """
    :param request: User choose a product
    :param product_id: id of the product
    :return: List of substitutes
    """
    product_chosen = Product.objects.get(pk=product_id)
    # Get substitutes for the product chosen
    category = product_chosen.category_id
    products = Product.objects.filter(category_id=category).values()
    substitutes = [product for product in products if product['nutriscore_grade'] < product_chosen.nutriscore_grade]
    # Get subs already save by the user
    user_id = request.user.id
    sub = Substitute.objects.filter(user_id=user_id).values('id')
    save_sub = [subs for subs in sub]
    save_sub = [subs['id'] for subs in save_sub]
    # Get nutriscore to display on pictures
    context = {
        'product': product_chosen,
        'substitutes': substitutes,
        'save_sub': save_sub,
    }
    return render(request, 'products/resultats.html', context)


def substitute(request, product_id):
    """
    :param request: Description button
    :param product_id: id of a product
    :return: Description page
    """
    substitute_chosen = Product.objects.get(pk=product_id)
    nutriscore = substitute_chosen.nutriscore_grade
    liste_nut = ['a','b','c','d','e']
    for i, value in enumerate(liste_nut):
        if nutriscore == liste_nut[i]:
            liste_nut[i] = value.upper()
    nut = ' '.join(liste_nut)
    context = {
        'substitute': substitute_chosen,
        'nutriscore': nut,
    }
    return render(request, 'products/informations.html', context)


@login_required
def save(request, sub_id):
    """
    :param request: save button
    :param sub_id: id of the substitute
    :return: Favorite list
    """
    fav = Product.objects.get(pk=sub_id)
    user = request.user.id
    try:
        if Substitute.objects.filter(pk=fav.id):
            print("Cet aliment est déjà dans vos favoris")
        else:
            add_favorite = Substitute(id=fav.id, created_at=timezone.now(),
                                      user_id=user)
            add_favorite.save()
            return show_favorites(request)
    except KeyError as e:
        print(e)


@login_required
def show_favorites(request):
    """
    :param request: Favorite button if user is login
    :return: Favorite page
    """
    user_id = request.user.id
    sub = Substitute.objects.filter(user_id=user_id).values('id')
    get_all_subs = []
    for i in sub:
        get_all_subs.append(i['id'])
    favorites = [favorite for favorite in Product.objects.all().values() if
                 favorite['id'] in get_all_subs]
    context = {
        'favorites': favorites,
    }
    return render(request, 'products/favorites.html', context)

