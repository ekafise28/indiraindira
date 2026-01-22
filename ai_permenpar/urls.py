from django.contrib import admin
from django.urls import path, include
from qa.views import chat_ui   # 👈 IMPORT DARI qa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("qa.urls")),
    path("chat/", chat_ui),
]