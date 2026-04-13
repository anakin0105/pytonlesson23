from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = CatalogConfig.name
urlpatterns = [
    path('', views.home, name='home'),  # главная
    path('catalog/', views.products_catalog, name='products_catalog'),  # каталог товаров
    path('contacts/', views.contacts, name='contacts'), # контакты
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # карточка товара
    path('add_product/', views.add_product, name='add_product'), # Новый товар
]

# ====================== MEDIA FILES (чтобы фото показывались) ======================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
