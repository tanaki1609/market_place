from rest_framework import serializers
from .models import Product, Category, Tag, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id reviews title price category tags tag_list category_name'.split()
        # exclude = 'id'.split()
        depth = 1

    def get_tag_list(self, product):
        # list_ = []
        # for tag in product.tags.all():
        #     list_.append(tag.name)
        # return list_
        return [tag.name for tag in product.tags.all()]
