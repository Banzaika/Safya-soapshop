from django.contrib import admin
from django.urls import path, include
from .views import Homeview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', Homeview.as_view(), name="home"),
    
]
