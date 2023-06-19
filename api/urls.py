from django.urls import path, re_path
from .views import ProviderView, DetailProviderView
from .views import QuotationView, DetailQuotationView

from .views import ProductView, DetailProductView

urlpatterns = [
    path('providers/', ProviderView.as_view(), name='lista-providers'),
    path('providers/<int:pk>/', DetailProviderView.as_view(), name='detail-providers'),

    path('products/', ProductView.as_view(), name='list-products'),
    path('products/<int:pk>/', DetailProductView.as_view(), name='detail-products'),

    path('products/<int:pk>/quotations/', QuotationView.as_view(), name='lista-quotations'),
    path('products/<int:pk>/quotations/<int:pk2>/', DetailQuotationView.as_view(), name='detail-quotations'),
]