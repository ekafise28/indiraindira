from django.urls import path
from .views import tanya_ai

urlpatterns = [
    path("tanya/", tanya_ai),
]
