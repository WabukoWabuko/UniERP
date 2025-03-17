from django.urls import path
from .views import NotifyView

urlpatterns = [
    path('notify/', NotifyView.as_view(), name='notify'),
]
