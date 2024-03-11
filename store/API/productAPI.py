from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models.product import Products
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductAPI(APIView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'image': openapi.Schema(type=openapi.TYPE_STRING),
            })
        )}
    )
    def get(self, request):
        products = Products.get_all_products()
        products_data = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category_id,
                'description': product.description,
                'image': product.image.url if product.image else None,
            }
            for product in products
        ]
        return Response(products_data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'image': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )}
    )
    def get_by_id(self, request, product_id):
        product = Products.get_products_by_id([product_id]).first()
        if product:
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category_id,
                'description': product.description,
                'image': product.image.url if product.image else None,
            }
            return Response(product_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)