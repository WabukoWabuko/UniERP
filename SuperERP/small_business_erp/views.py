from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BusinessUser

class SmallBusinessDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not BusinessUser.objects.filter(user=request.user).exists():
            return Response({'error': 'Not authorized for Small Business ERP'}, status=403)
        return Response({'message': 'Welcome to Small Business ERP Dashboard!'})
