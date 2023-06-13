from rest_framework.permissions import (BasePermission, AllowAny, IsAuthenticated)
from gbm_auth.models import AppUser as User


class GbmAdmin(BasePermission):

    @staticmethod
    def is_admin(request):
        if not request.user.is_authenticated:
            return False

        email = request.user.email
        try:
            user = User.objects.get(email=email)
            return user.is_admin
        except User.DoesNotExist:
            return False

