from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('main/', views.DashboardView.as_view(), name='dashboard'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('modify/', views.ModifyUserView.as_view(), name='modify_user'),
]