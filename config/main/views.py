from django.shortcuts import render
from django.http import Http404
from .models import Cart, Product, Category
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def category(request, slug):
    supergroups = {'for-body': (3, 4 , 5), 'for-hair': (2, 6), 'soaps': (1,)}
    categories = {'for-body': 'Для тела', 'for-hair': 'Для волос', 'soaps': 'Мыло'}
    user = request.user
    if slug in supergroups:
        products = Product.objects.filter(category__id__in=supergroups[slug])
    else:
        raise Http404('Такой категории еще нет...')
    сurrent_category = categories[slug]
    products_in_cart = []

    if user.is_authenticated:
        #collect products
        cart = Cart.objects.get_or_create(user=user)[0]
        products_in_cart += cart.get_products_id_in_cart()
    context = {"products": products, 'current_category': сurrent_category, "categories": categories, "cart": products_in_cart}
    return render(request, 'main/categories.html', context)


def product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "main/product.html")

def increase(request):
    print(request)
