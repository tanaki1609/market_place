from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
    # Step 1: Collect data of products from DB
    products = Product.objects\
        .select_related('category')\
        .prefetch_related('tags', 'reviews').all()

    # Step 2: Reformat(Serialize) of products
    data = ProductSerializer(products, many=True).data

    # Step 3: Return data as JSON
    return Response(data=data)


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
