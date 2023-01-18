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
    image = models.ForeignKey(ProductShots, verbose_name="Фото товара")
    components = models.ManyToManyField(Component, verbose_name="Составляющее", on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь")
    products = models.ManyToManyField(Product, verbose_name="Товар")
    credit = models.DecimalField(max_digits=6, decimal_places=2)

