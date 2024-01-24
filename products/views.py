from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status


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
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.in_stock = request.data.get('in_stock')
        product.is_active = request.data.get('is_active')
        product.category_id = request.data.get('category_id')
        product.tags.set(request.data.get('tags'))
        product.save()
        return Response(data={'product_id': product.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        # Step 1: Collect data of products from DB
        products = Product.objects \
            .select_related('category') \
            .prefetch_related('tags', 'reviews').all()

        # Step 2: Reformat(Serialize) of products
        data = ProductSerializer(products, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)
    elif request.method == 'POST':
        # Step 1. Get data from request body
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        in_stock = request.data.get('in_stock')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')

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
