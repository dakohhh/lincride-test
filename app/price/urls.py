from . import views
from django.urls import path


urlpatterns = [
    path('', views.FareCalculatorView.as_view(), name='fare-calculator'),
]