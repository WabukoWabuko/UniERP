from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.utils import ERPAuthentication
from education_erp.models import EducationUser
from small_business_erp.models import BusinessUser

class DashboardView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user  # Unwrap the ERP user
        available_erps = []

        if isinstance(user, EducationUser):
            available_erps.append({
                'id': 'education',
                'name': 'Education ERP',
                'url': '/dashboard/education'
            })
        elif isinstance(user, BusinessUser):
            available_erps.append({
                'id': 'small-business',
                'name': 'Small Business ERP',
                'url': '/dashboard/small-business'
            })

        return Response({'available_erps': available_erps})
