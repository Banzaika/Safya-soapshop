# Generated by Django 4.1.5 on 2023-02-28 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_product_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество в наличии'),
        ),
    ]
