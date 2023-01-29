from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField("Название", max_length=150)

class ProductShots(models.Model):
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(upload_to='product_shots/')

class Component(models.Model):
    name = models.CharField(max_length=150)

class Product(models.Model):
    name = models.CharField("Название", max_length=250)
    description = models.TextField("Описание")
    price = models.DecimalField(verbose_name="Цена", max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    poster = models.ImageField(upload_to="posters/")
    image = models.ForeignKey(ProductShots, verbose_name="Фото товара", on_delete=models.CASCADE)
    components = models.ManyToManyField(Component, verbose_name="Составляющее")

class Cart_relation(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    products = models.ManyToManyField("Product_for_cart", verbose_name="Товар")

class Product_for_cart(models.Model):
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Количество")

    
