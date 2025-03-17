from django.urls import path
from .views import EducationDashboardView, StudentListView, StudentDetailView, StaffListView, StaffDetailView, PayrollOverviewView

urlpatterns = [
    path('dashboard/', EducationDashboardView.as_view(), name='education_dashboard'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/<int:student_id>/', StudentDetailView.as_view(), name='student_detail'),
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:staff_id>/', StaffDetailView.as_view(), name='staff_detail'),
    path('payroll/', PayrollOverviewView.as_view(), name='payroll_overview'),
]
