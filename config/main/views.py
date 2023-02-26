from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from .orm_requests import get_products_by_supergroup, get_product_ides_in_cart_of, increase_product, decrease_product, remove_product_from_cart, get_relation_in_cart_of, get_products_in_cart_of, get_cart_relations_by_ides_of_
from .orm_requests import get_orders_of, confirm_to_order_delivery, create_order, create_order_relations, get_new_paid_orders, change_paid_status_from_order, delete2order
from .work_with_yookassa import create_payment
from django.views.decorators.csrf import csrf_exempt
import json
from yookassa.domain.common import SecurityHelper
from .serializers import OrderSerializer


def home(request):
    return render(request, 'home.html')

def about_shop(request):
    return render(request, 'main/about-shop.html')

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
    """Product card"""
    user = request.user
    product = Product.objects.get(id=id)

    components = [component.name for component in product.components.all()]
    components = ', '.join(components).capitalize()
    count_of_product_in_cart = 0
    product_in_cart = False
    if user.is_authenticated:
        product_in_cart = id in get_product_ides_in_cart_of(user)
        if product_in_cart:
            count_of_product_in_cart = get_relation_in_cart_of(user, id).amount
    context = {'product_in_cart': product_in_cart, 'product': product, 'count_of_product_in_cart': count_of_product_in_cart, "components": components}
    return render(request, "main/product.html", context)
 

def login_required_without_next(func):
    """decorator for redirect to login page without ?next"""
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
    if request.body:
        product_id = int(request.body.decode("utf-8"))
        increase_product(request.user, product_id)
        return JsonResponse({"success": True})


@login_required_without_next #к сожалению, мне нужен без якоря ?next
#потому что пользователь не должен посещать маршрут для этого представления
def decrease(request):
    """decrease count of product in cart"""
    user = request.user
    if request.body:
        product_id = int(request.body.decode("utf-8"))
        decrease_product(user, product_id)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required_without_next #к сожалению, мне нужен без якоря ?next
def clear(request):
    """remove product from cart"""
    user = request.user
    if request.body:
        product_id = int(request.body.decode("utf-8"))
        remove_product_from_cart(user, product_id)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

@login_required_without_next
def checkout(request):
    if request.body:
        relation_ides = request.body.decode('utf-8').split(',')
        request.session['relation_ides'] = relation_ides
        return redirect('ordering')
    else: 
        return JsonResponse({"success": False})

@login_required_without_next
def ordering(request):
    return render(request, 'main/checkout.html')

@login_required_without_next
def pay(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    patronymic = request.POST['patronymic']
    phone = request.POST['phone']
    address = request.POST['address']
    postcode = request.POST['ADDRESS_HOME_ZIP']
    user = request.user
    relation_ides = []
    # GETTING RELATIONS FROM SESSION 
    if 'relation_ides' in request.session.keys():
        relation_ides = request.session['relation_ides']
        del request.session['relation_ides']
    relations = get_cart_relations_by_ides_of_(user, relation_ides)


    #create order
    order = create_order(lastname, firstname, patronymic, postcode, address, phone, user, relations)
    create_order_relations(user, order, relations)
    price = order.common_price

    # FORMATION OF DESCRIPTION
    description = f'Покупка в Safiya на сумму {price}'

    payment_id, confirmation_url = create_payment(price, description)
    
    order.payment_id = payment_id
    order.save()

    return HttpResponseRedirect(confirmation_url)
@csrf_exempt
def new_orders(request):
    token = json.loads(request.body)["token"]
    if token == 'a;sldkfjal;ksdjfadjsf;lasdjpofi23412j1;23k4jl1;23k4':
        orders = get_new_paid_orders()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=400)

def get_ip_address(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def notifications(request):
    # checking by ip address
    ip = get_ip_address(request)
    if ip and not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    request_body = json.loads(request.body)
    payment = request_body['object']
    payment_id = payment['id']
    print(payment['status'])
    if payment['status'] == 'succeeded':
        change_paid_status_from_order(payment_id)
    elif payment['status'] == 'canceled':
       delete2order(payment_id)
    return HttpResponse(status=200)


@login_required_without_next
def orders(request):
    user = request.user
    orders = get_orders_of(user)
    context = {'orders': orders}
    return render(request, 'main/orders.html', context)


def delivery_confirmation(request):
    if request.body:
        order_id = int(request.body.decode('utf-8'))
        if confirm_to_order_delivery(request.user, order_id):
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


    