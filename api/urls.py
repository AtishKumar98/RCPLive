from django.urls import path
from django.contrib.auth import views as auth_views
# from django.conf.urls import url
from . import views



urlpatterns = [
    path('product/',views.ProductList, name='api'),
]