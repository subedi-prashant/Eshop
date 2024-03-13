from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models.customer import Customer
from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LoginAPI(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
            },
        ),
        responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message indicating successful login'),
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the logged-in customer'),
            },
        )}
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        customer = Customer.get_customer_by_email(email)
        
        if customer:
            if check_password(password, customer.password):
                request.session['customer'] = customer.id
                return Response({'message': 'Login successful', 'customer_id': request.session['customer']}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
