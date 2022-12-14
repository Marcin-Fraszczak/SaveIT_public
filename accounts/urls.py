from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('main/', views.DashboardView.as_view(), name='dashboard'),
    path('register/', views.RegisterView.as_view(), name='register'),
]