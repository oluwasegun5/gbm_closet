from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (ChangePasswordViewSet, UserViewSet)
from rest_framework.routers import DefaultRouter
from rest_framework import routers


router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()

app_router.register('users', UserViewSet, 'users')
app_router.register('change-password/<int:pk>', ChangePasswordViewSet, 'change-password')


urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(app_router.urls)),
]
