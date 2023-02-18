from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from .orm_questions import get_products_by_supergroup, get_product_ides_in_cart_of, increase_product, decrease_product, remove_product_from_cart, get_relation_in_cart_of, get_cart_of, get_products_in_cart_of


def home(request):
    return render(request, 'home.html')


def category(request, slug):
    """Страница со списком товаров отфильтрованных по категориям"""
    user = request.user

    categories = {'for-body': 'Для тела',
                  'for-hair': 'Для волос', 'soaps': 'Мыло'}
    сurrent_category = categories[slug]
    products = get_products_by_supergroup(slug)

    products_in_cart = []
    if user.is_authenticated:
        products_in_cart += get_product_ides_in_cart_of(user)

    context = {"products": products, 'current_category': сurrent_category,
               "categories": categories, "cart": products_in_cart}
    return render(request, 'main/categories.html', context)


def product(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    count_of_product_in_cart = 0
    product_in_cart = False
    if user.is_authenticated:
        product_in_cart = id in get_product_ides_in_cart_of(user)
        if product_in_cart:
            count_of_product_in_cart = get_relation_in_cart_of(user, id).amount
    context = {'product_in_cart': product_in_cart, 'product': product, 'count_of_product_in_cart': count_of_product_in_cart}
    return render(request, "main/product.html", context)
 

def login_required_without_next(func):
    """for redirect to login page without ?next"""
    def inner(request):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return func(request)
    return inner


@login_required
def cart(request):
    relations = get_products_in_cart_of(request.user)
    context = {"relations": relations}
    return render(request, 'main/cart.html', context)

@login_required_without_next #я бы мог использовать login_required, но ,к сожалению, мне нужен без якоря ?next
#потому что пользователь не должен посещать маршрут для этого представления
def increase(request):
    """increase count of product in cart """
    product_id = int(request.body.decode("utf-8"))
    increase_product(request.user, product_id)
    return JsonResponse({"success": 'True'})


@login_required_without_next #к сожалению, мне нужен без якоря ?next
#потому что пользователь не должен посещать маршрут для этого представления
def decrease(request):
    """decrease count of product in cart"""
    user = request.user
    if not user.is_authenticated:
        return redirect('account_login')

    product_id = int(request.body.decode("utf-8"))
    decrease_product(user, product_id)
    return JsonResponse({"success": 'True'})


@login_required_without_next #к сожалению, мне нужен без якоря ?next
def clear(request):
    """remove product from cart"""
    user = request.user
    if not user.is_authenticated:
        return redirect('account_login')

    product_id = int(request.body.decode("utf-8"))
    remove_product_from_cart(user, product_id)
    return JsonResponse({"success": 'True'})


