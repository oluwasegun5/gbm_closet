from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
import store.views as sv

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()

app_router.register('products', sv.ProductViewSet, 'product')
app_router.register('carts', sv.CartViewSet, 'cart')

urlpatterns = [
    path('', include(app_router.urls)),
]