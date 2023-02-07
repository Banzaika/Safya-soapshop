from django.shortcuts import render
from django.http import Http404
from .models import Cart_relation, Product, Category
from django.contrib.auth.decorators import login_required


def home(request):
    user = request.user
    if user.is_authenticated:
        relations = Cart_relation.objects.filter(user=user)
        context = {"relations": relations}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')

def category(request, slug):
    supergroups = {'for-body': (3, 4 , 5), 'for-hair': (2, 6), 'soaps': (1,)}
    categories = {'for-body': 'Для тела', 'for-hair': 'Для волос', 'soaps': 'Мыло'}
    if slug in supergroups:
        products = Product.objects.filter(category__id__in=supergroups[slug])
    else:
        raise Http404('Такой категории еще нет...')
    categories_names = categories.values()
    сurrent_category = categories[slug]
    context = {"products": products, 'current_category': сurrent_category, "categories": categories_names}
    return render(request, 'main/categories.html', context)


def product(request, pk):
    product = Product.objects.get(pk=pk)

    return render(request, "main/product.html")
