from . import views
from django.urls import path


urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('session/', views.SessionAPIView.as_view(), name='session'),
]
