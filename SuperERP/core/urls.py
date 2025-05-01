from django.contrib import admin
from django.urls import path, include
from dashboard.views import DashboardView, EducationDashboardView, SchedulingView, StaffManagementView, LmsDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard-hub'),
    path('api/dashboard/education/', EducationDashboardView.as_view(), name='education-dashboard'),
    path('api/dashboard/education/scheduling/', SchedulingView.as_view(), name='scheduling'),
    path('api/dashboard/education/scheduling/<int:fee_id>/', SchedulingView.as_view(), name='scheduling-update'),
    path('api/dashboard/education/staff/', StaffManagementView.as_view(), name='staff-management'),
    path('api/dashboard/education/lms/', LmsDashboardView.as_view(), name='lms-dashboard'),
]
