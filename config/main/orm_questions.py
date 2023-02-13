from .models import Cart_relation, Product, Category
from django.http import Http404


def get_cart_of(user):
    return Cart_relation.objects.filter(user=user)


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
        raise Http404('Такой категории еще нет...')
    return products


def increase_product(user, id):
    # increase count of product in cart of user
    product_ides = get_product_ides_in_cart_relations_of(user)
    if id in product_ides:
        relation = get_relation_in_cart_of(user, id)
        relation.amount += 1
        print('increase')
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
            print('decrease')
            relation.save()


def remove_product_from_cart(user, id):
    product_ides = get_product_ides_in_cart_relations_of(user)
    if id in product_ides:
        relation = get_relation_in_cart_of(user, id)
        relation.amount = 0
        print('remove')
        relation.save()


# def change_cart(user, move, id):
#     product_ides = get_product_ides_in_cart_of(user)
#     #increase count of product in cart of user
#     if move == 1:
#         if id in product_ides:
#             relation = get_relation_in_cart_of(user, id)
#             relation.amount += 1
#             relation.save()
#         else:
#             product = Product.objects.get(id=id)
#             Cart_relation.objects.create(user=user, product=product, amount=1)

#     #decrease count of product in cart of user
#     elif move == -1:
#         if id in product_ides:
#             relation = get_relation_in_cart_of(user, id)
#             amount = relation.amount
#             if amount > 0:
#                 relation.amount -= 1
#                 print('decrease')
#                 relation.save()
#     #remove product from cart of user
#     else:
#         if id in product_ides:
#             relation = get_relation_in_cart_of(user, id)
#             relation.amount = 0
#             print("clear")
#             relation.save()
