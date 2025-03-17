from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from education_erp.models import EducationUser
from small_business_erp.models import BusinessUser
from .utils import ERPUserWrapper
from .serializers import ERPAuthTokenSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        erp_id = request.data.get('erp_id')

        if not all([email, password, erp_id]):
            return Response({'error': 'All fields (email, password, erp_id) are required'}, status=400)

        user = None
        if erp_id == 'education':
            try:
                user = EducationUser.objects.get(email=email)
                if not user.check_password(password):
                    user = None
            except EducationUser.DoesNotExist:
                user = None
        elif erp_id == 'small-business':
            try:
                user = BusinessUser.objects.get(email=email)
                if not user.check_password(password):
                    user = None
            except BusinessUser.DoesNotExist:
                user = None
        else:
            return Response({'error': 'Invalid ERP ID'}, status=400)

        if user is None:
            return Response({'error': f'Invalid credentials for {erp_id} ERP'}, status=401)

        wrapped_user = ERPUserWrapper(user, erp_id)
        token = ERPAuthTokenSerializer.get_token(wrapped_user)  # Pass wrapped user with erp_id
        return Response({
            'refresh': str(token),
            'access': str(token.access_token),
            'erp_id': erp_id,
        })

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

        if erp_id == 'education':
            if EducationUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered in Education ERP'}, status=400)
            user = EducationUser(email=email)
            user.set_password(password)
            user.save()
        elif erp_id == 'small-business':
            if BusinessUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered in Small Business ERP'}, status=400)
            user = BusinessUser(email=email)
            user.set_password(password)
            user.save()
        else:
            return Response({'error': 'Invalid ERP ID'}, status=400)

        wrapped_user = ERPUserWrapper(user, erp_id)
        token = ERPAuthTokenSerializer.get_token(wrapped_user)  # Pass wrapped user with erp_id
        return Response({
            'refresh': str(token),
            'access': str(token.access_token),
            'message': 'Registration successful',
            'erp_id': erp_id,
        }, status=201)
