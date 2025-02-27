from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_NAME"])
        
        if access_token:
            try:
                validated_token = AccessToken(access_token)  # ✅ Decode token properly
                return self.get_user(validated_token=validated_token), validated_token
            except Exception:
                return None  # Invalid token

        return None

from rest_framework_simplejwt.tokens import RefreshToken
# Generate JWT Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

