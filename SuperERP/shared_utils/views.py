from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail

class NotifyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subject = request.data.get('subject', 'SuperERP Notification')
        message = request.data.get('message', 'You’ve got a new update!')
        recipient = request.user.email

        send_mail(
            subject,
            message,
            'basilwabbs@gmail.com',  # Replace with your email
            [recipient],
            fail_silently=True,  # Console backend for dev
        )
        return Response({'message': 'Notification sent!'})
