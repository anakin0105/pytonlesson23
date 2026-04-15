
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import (
    HomePageView,
    ProductsCatalogView,
    ProductDetailView,
    ProductCreateView,
    ContactsView,
)

app_name = 'catalog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('catalog/', ProductsCatalogView.as_view(), name='products_catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]

# ====================== MEDIA FILES (чтобы фото показывались) ======================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
