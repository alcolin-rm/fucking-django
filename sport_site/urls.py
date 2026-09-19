from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('matches/', include('matches.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('matches/', include('matches.urls')),
    path('accounts/', include('matches.auth_urls')),   # <-- регистрация/логин/выход
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)