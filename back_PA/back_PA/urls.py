from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('back_log.urls')),  # Incluindo as URLs do app back_log
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Servindo arquivos estáticos
