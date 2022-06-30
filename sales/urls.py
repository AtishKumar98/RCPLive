from django.urls import path 
from .views import *


app_name = 'sales'




urlpatterns = [
    path('',home_view,name = 'sales'),
    path('sales_home/',SalesView.as_view(),name = 'list'),
    path('sales/<pk>/',SalesDetailView.as_view(),name = 'details')
]


