from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.utils import ERPAuthentication
from .models import BusinessUser

class SmallBusinessDashboardView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isinstance(request.user.user, BusinessUser):  # Unwrap the ERP user
            return Response({'error': 'Not authorized for Small Business ERP'}, status=403)
        return Response({'message': 'Welcome to Small Business ERP Dashboard!'})
