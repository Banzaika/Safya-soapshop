from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", 'get_image', 'weight')
    readonly_fields = ["get_image",]

    def get_image(sefl, obj):
        return mark_safe(f'<img src="{obj.poster.url}" weight="80" height="80">')

    get_image.short_description = 'Изображение'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )


admin.site.register(ProductShots)
class ProductShotsAdmin(admin.ModelAdmin):
    list_display = ("name", 'get_image',)
    readonly_fields = ["get_image",]

    def get_image(sefl, obj):
        return mark_safe(f'<img src="{obj.image.url}" weight="80" height="80">')

    get_image.short_description = 'Изображение'    


admin.site.register(Component)

admin.site.register(Cart_relation)
admin.site.register(Order_relation)
class Order_relationAdmin(admin.ModelAdmin):
    list_display = ["product", 'amount']
admin.site.register(Order)

class Order_relationInline(admin.TabularInline):
    model = Order_relation
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ("lastname", "name", "patronymic", 'phone',  'common_price')
    inlines = [Order_relationInline,]



admin.site.site_title = "Safiya"
admin.site.site_header = "Safiya"