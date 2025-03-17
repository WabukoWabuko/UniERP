from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from education_erp.models import EducationUser
from small_business_erp.models import BusinessUser

class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        available_erps = []

        # Check which ERPs the user is registered for
        if EducationUser.objects.filter(user=user).exists():
            available_erps.append({
                'id': 'education',
                'name': 'Education ERP',
                'url': '/dashboard/education'
            })
        if BusinessUser.objects.filter(user=user).exists():
            available_erps.append({
                'id': 'small-business',
                'name': 'Small Business ERP',
                'url': '/dashboard/small-business'
            })
        # Add other 8 ERPs later

        return Response({'available_erps': available_erps})
