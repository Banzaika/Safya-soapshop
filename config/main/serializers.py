from rest_framework.serializers import ModelSerializer
from .models import Order, Order_relation
from rest_framework import serializers

class Order_relationSerializer(ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_category = serializers.CharField(source='product.category.name')
    class Meta:
        model = Order_relation
        fields = ['product_category', 'product_name','amount']

class OrderSerializer(ModelSerializer):
    order_relations = Order_relationSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['lastname', 'name', 'patronymic', 'phone', 'street_address', 'postcode', 'common_price', 'order_relations', ]



