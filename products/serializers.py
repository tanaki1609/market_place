from rest_framework import serializers
from .models import Product, Category, Tag, Review
from rest_framework.exceptions import ValidationError


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


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=10, max_value=1000000)
    in_stock = serializers.IntegerField()
    is_active = serializers.BooleanField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category not found!')
        return category_id

    # def validate_tags(self, tags):
    #     for tag_id in tags:  # [1,2,100]
    #         try:
    #             Tag.objects.get(id=tag_id)
    #         except Tag.DoesNotExist:
    #             raise ValidationError('Tag not found!')
    #     return tags
