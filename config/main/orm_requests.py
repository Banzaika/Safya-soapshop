from .models import Cart_relation, Product, Order, Order_relation
from django.http import Http404
from django.db.models import Sum

def get_cart_of(user):
    return Cart_relation.objects.filter(user=user)

def get_products_in_cart_of(user):
    return Cart_relation.objects.filter(user=user, amount__gt = 0)

def get_relation_in_cart_of(user, id):
    relations = get_cart_of(user)
    for relation in relations:
        if relation.product.id == id:
            return relation


def get_product_ides_in_cart_of(user):
    ides = []
    for relation in get_cart_of(user):
        id = relation.product.id
        amount = relation.amount
        if amount > 0:
            ides.append(id)
    return ides


def get_product_ides_in_cart_relations_of(user):
    ides = []
    for relation in get_cart_of(user):
        ides.append(relation.product.id)
    return ides


def get_products_by_supergroup(slug):
    supergroups = {'for-body': (3, 4, 5), 'for-hair': (2, 6), 'soaps': (1,)}
    if slug in supergroups:
        products = Product.objects.filter(category__id__in=supergroups[slug])
    else:
        raise Http404()
    return products


def increase_product(user, id):
    # increase count of product in cart of user
    product_ides = get_product_ides_in_cart_relations_of(user)
    if id in product_ides:
        relation = get_relation_in_cart_of(user, id)
        relation.amount += 1
        relation.save()
    else:
        product = Product.objects.get(id=id)
        Cart_relation.objects.create(user=user, product=product, amount=1)


def decrease_product(user, id):
    # decrease count of product in cart of user
    product_ides = get_product_ides_in_cart_relations_of(user)
    if id in product_ides:
        relation = get_relation_in_cart_of(user, id)
        amount = relation.amount
        if amount > 0:
            relation.amount -= 1
            relation.save()


def remove_product_from_cart(user, id):
    product_ides = get_product_ides_in_cart_relations_of(user)
    if id in product_ides:
        relation = get_relation_in_cart_of(user, id)
        relation.amount = 0
        relation.save()



def get_cart_relations_by_ides_of_(user, ides):
    return Cart_relation.objects.filter(user=user, id__in=ides)

def summing_of_prices_in_cart(relations):
    result = 0
    for relation in relations:
        result += relation.amount * relation.product.price
    return result

def create_order(lastname, firstname, patronymic, postcode, address, phone, user, relations):
    common_price = summing_of_prices_in_cart(relations)
    order = Order.objects.create(user=user, lastname=lastname, name=firstname, patronymic=patronymic, phone=phone, street_address=address, postcode=postcode, common_price=common_price)
    return order

def create_order_relation(user, product, amount, order):
    Order_relation.objects.create(user=user, product=product, amount=amount, order_pack=order)

def create_order_relations(user, order, cart_relations):
    for cart_relation in cart_relations:
        product = cart_relation.product
        amount = cart_relation.amount
        create_order_relation(user, product, amount, order)

def get_orders_of(user):
    return Order.objects.filter(user=user, paid=True).order_by('status')

def get_new_paid_orders():
    orders = Order.objects.filter(paid=True, new=True)
    for order in orders:
        order.new = False
        order.save()
    return orders

def confirm_to_order_delivery(user, order_id):
    order = Order.objects.get(id=order_id, user=user)
    if order:
        order.status = 'c'
        order.save()
        return True
    return False

def change_paid_status_from_order(id):
    order = Order.objects.get(payment_id=id)
    order.paid = True
    order.save()

def delete2order(payment_id):
    Order.objects.get(payment_id=payment_id).delete()
    print('end')