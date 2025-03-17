from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import EducationUser

class EducationDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if user is registered for this ERP
        if not EducationUser.objects.filter(user=request.user).exists():
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        return Response({'message': 'Welcome to Education ERP Dashboard!'})
