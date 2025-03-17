from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # Use email as username for simplicity, since allauth might expect it
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)  # Log the user in for session (optional for API, but good for testing)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid email or password'}, status=401)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not email or not password or not confirm_password:
            return Response({'error': 'All fields are required'}, status=400)
        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=400)
        if User.objects.filter(email=email).exists():  # Check email directly
            return Response({'error': 'Email already registered'}, status=400)

        # Create user with email as username for consistency
        user = User.objects.create_user(username=email, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        login(request, user)  # Auto-login after register
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Registration successful'
        }, status=201)
