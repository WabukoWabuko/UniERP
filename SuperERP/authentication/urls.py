from django.urls import path
from .views import LoginView  # Assuming LoginView exists from our previous work

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
