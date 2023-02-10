from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('category/<slug:slug>', views.category, name='categories'),
    path('product/<int:pk>', views.product, name='product'),
    path('increase', views.increase)
    # path('cart/', views.cart, name='cart'),
]