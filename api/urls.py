from django.urls import path, re_path
from .views import ProviderView, DetailProviderView
from .views import QuotationView, DetailQuotationView

from .views import ProductView, DetailProductView
from .views import MarkView, DetailMarkView
from .views import ModelView, DetailModelView
from .views import CategoryView, DetailCategoryView

urlpatterns = [
    path('providers/', ProviderView.as_view(), name='lista-providers'),
    path('providers/<int:pk>/', DetailProviderView.as_view(), name='detail-providers'),

    path('products/', ProductView.as_view(), name='list-products'),
    path('products/<int:pk>/', DetailProductView.as_view(), name='detail-products'),

    path('marks/', MarkView.as_view(), name='list-marks'),
    path('marks/<int:pk>/', DetailMarkView.as_view(), name='detail-marks'),

    path('models/', ModelView.as_view(), name='list-models'),
    path('models/<int:pk>/', DetailModelView.as_view(), name='detail-models'),

    path('categories/', CategoryView.as_view(), name='list-categories'),
    path('categories/<int:pk>/', DetailCategoryView.as_view(), name='detail-categories'),

    path('products/<int:pk>/quotations/', QuotationView.as_view(), name='lista-quotations'),
    path('products/<int:pk>/quotations/<int:pk2>/', DetailQuotationView.as_view(), name='detail-quotations'),
]