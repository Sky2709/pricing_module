# pricing/urls.py
from django.urls import path
from .views import CalculatePriceAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/calculate-price/', CalculatePriceAPI.as_view(), name='calculate-price'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
