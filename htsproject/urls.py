from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path("", include("ecomapp.urls")),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'ecomapp.views.handle404'
handler500 = 'ecomapp.views.handle500'