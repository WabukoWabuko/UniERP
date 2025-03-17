from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from education_erp.models import EducationUser
from small_business_erp.models import BusinessUser

class ERPUserWrapper:
    def __init__(self, user, erp_id):
        self.user = user
        self._erp_id = erp_id
        self.is_authenticated = True
        self.is_anonymous = False

    @property
    def id(self):
        return self.user.id

    @property
    def email(self):
        return self.user.email

    def __getattr__(self, name):
        return getattr(self.user, name)

def get_erp_user(user_id, erp_id):  # Changed to use ID from token
    if erp_id == 'education':
        try:
            return ERPUserWrapper(EducationUser.objects.get(id=user_id), erp_id)
        except EducationUser.DoesNotExist:
            return AnonymousUser()
    elif erp_id == 'small-business':
        try:
            return ERPUserWrapper(BusinessUser.objects.get(id=user_id), erp_id)
        except BusinessUser.DoesNotExist:
            return AnonymousUser()
    return AnonymousUser()

class ERPAuthentication(BaseJWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            erp_id = validated_token.get('erp_id')
            if not erp_id:
                raise InvalidToken('Token missing erp_id')
            return get_erp_user(user_id, erp_id)
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')
