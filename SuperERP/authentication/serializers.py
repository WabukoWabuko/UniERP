from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class ERPAuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Expect user to be an ERPUserWrapper instance
        token = RefreshToken.for_user(user)
        token['erp_id'] = user._erp_id  # Use the erp_id from the wrapped user
        return token
