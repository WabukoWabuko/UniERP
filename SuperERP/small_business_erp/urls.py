from django.urls import path
from .views import SmallBusinessDashboardView

urlpatterns = [
    path('dashboard/', SmallBusinessDashboardView.as_view(), name='small_business_dashboard'),
]
