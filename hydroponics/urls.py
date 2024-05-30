from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("hydroapi.urls")),
    path("api/hydro/", include("hydroapi.urls"))
]
