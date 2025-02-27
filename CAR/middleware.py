from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if "access_token" in request.COOKIES:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {request.COOKIES['access_token']}"
