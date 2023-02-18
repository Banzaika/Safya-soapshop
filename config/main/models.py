from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
        
class Category(models.Model):
    name = models.CharField("Название", max_length=150)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

class ProductShots(models.Model):
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(upload_to='product_shots/')
    product = models.ForeignKey("Product", verbose_name="Товар", on_delete=models.CASCADE, blank=True, null=True)

    class Meta: 
        verbose_name = 'Фотография товара'
        verbose_name_plural = "Фотографии товара"
    
    def __str__(self):
        return self.name
    

class Component(models.Model):
    name = models.CharField(max_length=150)
    class Meta: 
        verbose_name = 'Составляющее косметики'
        verbose_name_plural = "Составляющие косметики"

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField("Название", max_length=250)
    description = models.TextField("Описание")
    price = models.IntegerField(verbose_name="Цена")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    poster = models.ImageField(upload_to="posters/")
    components = models.ManyToManyField(Component, verbose_name="Составляющее")
    weight = models.PositiveIntegerField('Вес товара', help_text='Указывать в граммах', default=0)

    def get_absolute_url(self):
        return reverse("product", kwargs={"id": self.pk})
    
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"


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
    
    class Meta: 
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"



class Cart_relation(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField("Количество")

    def __str__(self):
        return f'{self.user.first_name} - {self.product.name}'
    

    class Meta: 
        verbose_name = 'Корзина'
        verbose_name_plural = "Корзины"


    
