from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-v2/', include('api_v2.urls')),
    path('api-v2-geek/', include('api_v2_geek_book.urls')),
    path('api-v3-crud/', include('api_v3_crud.urls')),
]
