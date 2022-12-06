from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('category/add/', views.AddCategoryView.as_view(), name='add_category'),
]