from django.contrib import admin     # ← add this line
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
]