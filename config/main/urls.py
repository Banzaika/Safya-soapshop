from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('products/', views.products, name='products'),
    path('category/<int:pk>', views.categories, name='categories'),
    path('product/<int:pk>', views.product, name='product'),
    ]