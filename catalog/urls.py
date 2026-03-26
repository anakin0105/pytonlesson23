from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = CatalogConfig.name
urlpatterns = [
    path("", home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
]

# ====================== MEDIA FILES (чтобы фото показывались) ======================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
