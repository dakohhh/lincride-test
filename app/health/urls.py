from . import views
from django.urls import path

urlpatterns = [
    path("", views.HealthView.as_view(), name="health")
]