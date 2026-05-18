from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import (
    HomePageView,
    ProductsCatalogView,
    ProductDetailView,
    ProductCreateView,
    ContactsView,
    MyProductsView,
    ProductUpdateView,  # ← добавь
    ProductDeleteView, CategoryProductsView,  # ← добавь
)

app_name = 'catalog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('catalog/', ProductsCatalogView.as_view(), name='products_catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('my_products/', MyProductsView.as_view(), name='my_products'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),   # ← добавь
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),  # ← добавь
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
