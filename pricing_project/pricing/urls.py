# pricing/urls.py
from django.urls import path
from .views import CalculatePriceAPI

urlpatterns = [
    path('api/calculate-price/', CalculatePriceAPI.as_view(), name='calculate-price'),
]

# pricing_project/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pricing/', include('pricing.urls')),
]