# Generated by Django 4.1.5 on 2023-01-30 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_remove_product_image_productshots_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('status', models.CharField(choices=[('a', 'Обрабатывается'), ('b', 'Отменен'), ('c', 'Передано в доставку'), ('d', 'Доставлено')], max_length=1, verbose_name='Статус')),
                ('products', models.ManyToManyField(to='main.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]