from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models.customer import Customer
from django.contrib.auth.hashers import check_password

class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        customer = Customer.get_customer_by_email(email)
        
        if customer:
            if check_password(password, customer.password):
                request.session['customer'] = customer.id
                return Response({'message': 'Login successful', 'customer_id': customer.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
