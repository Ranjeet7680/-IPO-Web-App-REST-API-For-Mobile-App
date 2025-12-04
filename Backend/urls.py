# ipo_platform/urls.py (root)
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ipo_api.views import IPOViewSet, CompanyViewSet, DocumentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'ipos', IPOViewSet, basename='ipo')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
