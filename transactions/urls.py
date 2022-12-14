from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('list/', views.ListTransactionView.as_view(), name='list_transaction'),
    path('modify/<int:pk>/', views.ModifyTransactionView.as_view(), name='modify_transaction'),
    path('delete/<int:pk>/', views.DeleteTransactionView.as_view(), name='delete_transaction'),
]

