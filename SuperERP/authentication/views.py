from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .utils import ERPAuthentication
import logging

logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        erp_id = request.data.get('erp_id', 'education')  # Default to education

        user = authenticate(request, username=email, password=password)
        if user and isinstance(user, ERPAuthentication):
            refresh = RefreshToken.for_user(user)
            logger.info(f"User {email} logged in with ERP ID: {erp_id}")
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'erp_id': erp_id
            })
        logger.error(f"Login failed for {email}")
        return Response({'error': 'Invalid credentials'}, status=401)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User {user.email} registered")
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            })
        logger.error(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.email} logged out")
            return Response({'message': 'Successfully logged out'})
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response({'error': str(e)}, status=400)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        logger.info(f"User profile accessed for {request.user.email}")
        return Response(serializer.data)
