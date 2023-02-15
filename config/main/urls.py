from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'), 
    path('category/<slug:slug>', views.category, name='categories'),
    path('product/<int:id>', views.product, name='product'),
    path('cart/increase', views.increase),
    path('cart/decrease', views.decrease),
    path('cart/clear', views.clear),
    path('cart/', views.cart, name='cart'),
    # path('cart/', views.cart, name='cart'),
]