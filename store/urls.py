from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()

app_router.register('product', ProductViewSet, 'product')

urlpatterns = [
    path('', include(app_router.urls)),
]