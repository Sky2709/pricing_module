# pricing/urls.py
from django.urls import path
from .views import CalculatePriceAPI

urlpatterns = [
    path('api/calculate-price/', CalculatePriceAPI.as_view(), name='calculate-price'),
]
