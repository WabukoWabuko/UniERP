from django.urls import path
from .views import EducationDashboardView

urlpatterns = [
    path('dashboard/', EducationDashboardView.as_view(), name='education_dashboard'),
]
