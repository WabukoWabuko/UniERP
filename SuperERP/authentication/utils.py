from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from education_erp.models import EducationUser

class ERPAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = self.get_authorization_header(request).decode('utf-8').split()[1]
        try:
            payload = self.get_validated_token(token)
            user_id = payload['user_id']
            erp_id = payload['erp_id']
            user = EducationUser.objects.get(id=user_id)

            if erp_id != 'education' or not isinstance(user, EducationUser):
                raise AuthenticationFailed('Invalid ERP user')

            # Check permissions
            required_permission = request.query_params.get('permission', None)
            if required_permission and not user.permissions.get(required_permission, False):
                raise AuthenticationFailed(f'Permission "{required_permission}" required')

            request.auth = payload
            return (user, token)
        except Exception as e:
            raise AuthenticationFailed(str(e))
