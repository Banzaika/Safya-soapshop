from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )


admin.site.register(ProductShots)


admin.site.register(Component)

admin.site.register(Cart_relation)
admin.site.register(Order_relation)
admin.site.register(Order)

