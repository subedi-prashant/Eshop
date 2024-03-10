from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer

class SignupAPI(APIView):
    def post(self, request):
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')
        phone = request.data.get('phone')
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Validation
        error_message = self.validate_customer_data(first_name, last_name, phone, email, password)
        if error_message:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Creating the customer object
        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
        customer.password = make_password(password)
        customer.save()


        # Return success response with user data
        user_data = {
            'id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'phone': customer.phone,
            'email': customer.email
        }
        return Response({'message': 'Signup successful', 'user': user_data}, status=status.HTTP_201_CREATED)

    def validate_customer_data(self, first_name, last_name, phone, email, password):
        error_message = None
        if not first_name or len(first_name) < 3:
            error_message = "First Name must be at least 3 characters long."
        elif not last_name or len(last_name) < 3:
            error_message = "Last Name must be at least 3 characters long."
        elif not phone or len(phone) < 10:
            error_message = "Phone Number must be at least 10 characters long."
        elif not email or len(email) < 5:
            error_message = "Email must be at least 5 characters long."
        elif not password or len(password) < 5:
            error_message = "Password must be at least 5 characters long."
        elif Customer.objects.filter(email=email).exists():
            error_message = "Email Address already exists."

        return error_message
