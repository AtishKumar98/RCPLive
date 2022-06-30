
from rest_framework import serializers
from EcartProducts.models import Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'