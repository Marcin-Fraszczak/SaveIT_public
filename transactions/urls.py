from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add/category/', views.AddCategoryView.as_view(), name='add_category'),
    path('list/category/', views.ListCategoryView.as_view(), name='list_category'),
    path('modify/category/<int:pk>/', views.ModifyCategoryView.as_view(), name='modify_category'),


    path('add/counterparty/', views.AddCounterpartyView.as_view(), name='add_counterparty'),
    path('list/counterparty/', views.ListCounterpartyView.as_view(), name='list_counterparty'),
    path('modify/counterparty/<int:pk>/', views.ModifyCounterpartyView.as_view(), name='modify_counterparty'),

    path('add/wallet/', views.AddWalletView.as_view(), name='add_wallet'),
    path('list/wallet/', views.ListWalletView.as_view(), name='list_wallet'),
    path('modify/wallet/<int:pk>/', views.ModifyWalletView.as_view(), name='modify_wallet'),


    path('add/transaction/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('list/transaction/', views.ListTransactionView.as_view(), name='list_transaction'),
    path('modify/transaction/<int:pk>/', views.ModifyTransactionView.as_view(), name='modify_transaction'),

]

