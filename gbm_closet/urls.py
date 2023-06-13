from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('gbm_auth.urls')),
    path('api/', include('store.urls'))
]
