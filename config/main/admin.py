from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

class Order_relationInline(admin.TabularInline):
    model = Order_relation
    readonly_fields = ['user', 'product', 'amount', 'order_pack']
    extra = 1

class ProductShotsInline(admin.TabularInline):
    model = ProductShots
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', "name")
    list_display_links = list_display


    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', "name", "price", 'get_image', 'weight')
    list_display_links = list_display
    list_filter = ('name', 'price', 'category')
    search_fields = ('name', 'description')
    readonly_fields = ["get_image",]
    inlines = (ProductShotsInline, )
    save_on_top = True

    def get_image(sefl, obj):
        return mark_safe(f'<img src="{obj.poster.url}" weight="80" height="80">')

    get_image.short_description = 'Изображение'




@admin.register(ProductShots)
class ProductShotsAdmin(admin.ModelAdmin):
    list_display = ("name", 'get_image',)
    readonly_fields = ["get_image",]

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" weight="80" height="80">')

    get_image.short_description = 'Изображение'    


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = list_display
    search_fields = ('name',)



admin.site.register(Cart_relation)

@admin.register(Order_relation)
class Order_relationAdmin(admin.ModelAdmin):
    model = Order_relation
    list_display = ["product", 'amount']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("lastname", "name", "patronymic", 'phone',  'common_price')
    list_display_links = list_display
    inlines = [Order_relationInline,]
    save_on_top = True



admin.site.site_title = "Safiya"
admin.site.site_header = "Safiya"