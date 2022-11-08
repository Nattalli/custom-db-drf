from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django_restful_admin import admin as api_admin


api = [
    path('', include('db.urls')),
    path('apiadmin/', api_admin.site.urls),
]

urlpatterns = [
    path('api/', include(api)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
