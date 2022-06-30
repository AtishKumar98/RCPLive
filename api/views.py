from django.shortcuts import render
from EcartProducts.models import Product
from .serializers import ProductSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
# Create your views here.


@api_view(['GET','POST'])
def ProductList(request):
    if request.method == 'GET':
        Plist=Product.objects.all()
        Pserializer=ProductSerializer(Plist,many=True)
        return Response(Pserializer.data)
    elif request.method == 'POST':
        Pserializer=ProductSerializer(data=request.data)
        if Pserializer.is_valid():
            Pserializer.save()
            return Response(Pserializer.data, status=status.HTTP_201_CREATED)
        return Response(Pserializer.errors, status=status.HTTP_400_BAD_REQUEST)

