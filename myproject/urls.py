from django.contrib import admin
from django.urls import path
from app.views import upload_image, view_images
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload-image/', upload_image, name='upload-image'),
    path('view-images/', view_images, name='view-images'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
