from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('add/', views.AddCategoryView.as_view(), name='add_category'),
    path('list/', views.ListCategoryView.as_view(), name='list_category'),
    path('modify/<int:pk>/', views.ModifyCategoryView.as_view(), name='modify_category'),
    # path('delete/<int:pk>/', views.DeleteCategoryView.as_view(), name='delete_category'),
]

