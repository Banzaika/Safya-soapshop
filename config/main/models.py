from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
        
class Category(models.Model):
    name = models.CharField("Название", max_length=150)

class ProductShots(models.Model):
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(upload_to='product_shots/')
    product = models.ForeignKey("Product", verbose_name="Товар", on_delete=models.CASCADE, blank=True, null=True)

class Component(models.Model):
    name = models.CharField(max_length=150)

class Product(models.Model):
    name = models.CharField("Название", max_length=250)
    description = models.TextField("Описание")
    price = models.IntegerField(verbose_name="Цена")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    poster = models.ImageField(upload_to="posters/")
    components = models.ManyToManyField(Component, verbose_name="Составляющее")

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUSES = (
        ('a', 'Обрабатывается'),
        ('b', 'Отменен'),
        ('c', 'Передано в доставку'),
        ('d', 'Доставлено'),
        )
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    products = models.ManyToManyField("Product", verbose_name="Товар")
    date = models.DateTimeField("Дата и время", auto_now_add=True)
    status = models.CharField("Статус", max_length=1, choices=STATUSES)

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    products = models.ManyToManyField("Product_for_cart", verbose_name="Товар")

    def get_products_id_in_cart(self):
        prod_id_in_cart = []
        for product_for_cart in self.products.all():
            prod_id_in_cart.append(product_for_cart.product.id)
        return prod_id_in_cart

class Product_for_cart(models.Model):
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Количество")

    
