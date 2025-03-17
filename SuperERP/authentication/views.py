from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from education_erp.models import EducationUser
from small_business_erp.models import BusinessUser

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
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
        erp_id = request.data.get('erp_id')

        if not all([email, password, confirm_password, erp_id]):
            return Response({'error': 'All fields (email, password, confirm_password, erp_id) are required'}, status=400)
        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        if erp_id == 'education':
            EducationUser.objects.create(user=user)
        elif erp_id == 'small-business':
            BusinessUser.objects.create(user=user)
        else:
            user.delete()  # Roll back if ERP not supported
            return Response({'error': 'Invalid ERP ID'}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Registration successful',
            'erp_id': erp_id,
        }, status=201)
