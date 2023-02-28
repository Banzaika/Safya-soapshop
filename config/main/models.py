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
    name = models.CharField('Название', max_length=150, help_text='Если картинка по какой-то причине не загрузится, то выводится этот текст')
    image = models.ImageField(upload_to='product_shots/')
    product = models.ForeignKey("Product", verbose_name="Товар", related_name='shots', on_delete=models.CASCADE, blank=True, null=True)

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
    amount = models.IntegerField('Количество в наличии', default=1)

    def get_absolute_url(self):
        return reverse("product", kwargs={"id": self.pk})
    
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"

class Order_relation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField("Количество")
    order_pack = models.ForeignKey("Order", verbose_name='Пакет товаров', on_delete=models.CASCADE, related_name='order_relations')

    def __str__(self):
        return f'{self.user} - {self.product} - {self.amount}'
    

    class Meta:
        verbose_name = 'Товар для заказа'
        verbose_name_plural = 'Товары для заказа'

class Order(models.Model):
    payment_id = models.CharField('Payment ID', max_length=255, null=True)
    STATUSES = (
        ('a', 'Обрабатывается'),
        ('b', 'Передано в доставку'),
        ('c', 'Доставлено'),
        )
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    #data for delivery
    lastname = models.CharField('Фамилия', max_length=200, default='Фамилия по умолчанию')
    name = models.CharField("Имя", max_length=200, default='Имя по умолчанию')
    patronymic = models.CharField('Отчество', max_length=200, default='Отчество по умолчанию')    
    phone = models.CharField('Номер телефона', max_length=12, default='Не задан')
    street_address = models.CharField('Почтовый адрес', max_length=400, default='Адрес по умолчанию')
    postcode = models.CharField('Почтовый индекс', max_length=50, default='Индекс по умолчанию')
    common_price = models.PositiveIntegerField('Итоговая цена', default=1)


    date = models.DateTimeField("Дата и время", auto_now_add=True)
    status = models.CharField("Статус", max_length=1, choices=STATUSES, default='a')

    track_number = models.CharField('Трек номер', max_length=30, blank=True, null=True)

    paid = models.BooleanField("Оплачено(Да/Нет)", default=False)
    new = models.BooleanField("Новый", default=True)

    def get_status(self):
        statuses = {
            self.STATUSES[0][0]:self.STATUSES[0][1],
            self.STATUSES[1][0]:self.STATUSES[1][1],
            self.STATUSES[2][0]:self.STATUSES[2][1]
        }
        return statuses[self.status]



    def __str__(self):
        return f'{self.lastname} {self.name} {self.patronymic} - {self.common_price}P'

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


    
