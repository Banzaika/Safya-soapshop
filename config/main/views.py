from django.shortcuts import render
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


@login_required()
def products(request):
    context = {"products": Product.objects.all()}
    return render(request, 'products.html', context)


def categories(request, pk):
    categories = Category.objects.all()
    current_category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=current_category)
    context = {"categories": categories,
               "current_category": current_category, "products": products}
    return render(request, 'main/categories.html', context)


def product(request, pk):
    product = Product.objects.get(pk=pk)
    context = {"product": product}
    return render(request, "main/product.html", context)
