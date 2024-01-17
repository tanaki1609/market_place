from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price __str__'.split()
        # exclude = 'id'.split()
