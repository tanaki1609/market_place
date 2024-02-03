from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product, Tag, Category
from .serializers import ProductSerializer, ProductValidateSerializer, \
    TagSerializer, CategorySerializer
from rest_framework import status


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class TagListCreateAPIView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination


class TagDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.in_stock = serializer.validated_data.get('in_stock')
        product.is_active = serializer.validated_data.get('is_active')
        product.category_id = serializer.validated_data.get('category_id')
        product.tags.set(serializer.validated_data.get('tags'))
        product.save()
        return Response(data={'product_id': product.id}, status=status.HTTP_201_CREATED)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects \
        .select_related('category') \
        .prefetch_related('tags', 'reviews').all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        # Step 1. Get data from request body
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        in_stock = serializer.validated_data.get('in_stock')
        is_active = serializer.validated_data.get('is_active')  # "y"
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # Step 2. Create product by received data
        product = Product.objects.create(title=title, description=description,
                                         price=price, in_stock=in_stock,
                                         is_active=is_active, category_id=category_id)
        product.tags.set(tags)
        product.save()

        # Step 3. Return response with created data and status
        return Response(data={'product_id': product.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # Step 1: Collect data of products from DB
        products = Product.objects \
            .select_related('category') \
            .prefetch_related('tags', 'reviews') \
            .filter(title__contains=request.query_params.get('search_word', ''))

        # Step 2: Reformat(Serialize) of products
        data = ProductSerializer(products, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)
    elif request.method == 'POST':
        # Step 0. Validate data
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        # Step 1. Get data from request body
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        in_stock = serializer.validated_data.get('in_stock')
        is_active = serializer.validated_data.get('is_active')  # "y"
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # Step 2. Create product by received data
        product = Product.objects.create(title=title, description=description,
                                         price=price, in_stock=in_stock,
                                         is_active=is_active, category_id=category_id)
        product.tags.set(tags)
        product.save()

        # Step 3. Return response with created data and status
        return Response(data={'product_id': product.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def test_api_view(request):
    json_object = {
        'int': 100,
        'float': 9.99,
        'text': 'hello',
        'dict': {
            'key': 'value'
        },
        'list': [1, 2, 3],
        'bool': True,
    }
    return Response(data=json_object)
