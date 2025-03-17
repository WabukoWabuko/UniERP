from django.contrib import admin
from django.urls import path, include
from authentication.views import LoginView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/education/', include('education_erp.urls')),
    path('api/small-business/', include('small_business_erp.urls')),
]
