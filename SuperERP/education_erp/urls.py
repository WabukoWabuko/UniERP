from django.urls import path
from .views import EducationDashboardView, StudentListView, StudentDetailView

urlpatterns = [
    path('dashboard/', EducationDashboardView.as_view(), name='education_dashboard'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/<int:student_id>/', StudentDetailView.as_view(), name='student_detail'),
]
