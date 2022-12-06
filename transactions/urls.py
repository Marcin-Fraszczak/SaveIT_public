from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add/category/', views.AddCategoryView.as_view(), name='add_category'),
    path('list/category/', views.ListCategoryView.as_view(), name='list_category'),
    path('add/counterparty/', views.AddCounterpartyView.as_view(), name='add_counterparty'),
    path('list/counterparty/', views.ListCounterpartyView.as_view(), name='list_counterparty'),
    # path('add/wallet/', views.AddWalletView.as_view(), name='add_wallet'),
    # path('list/wallet/', views.ListWalletView.as_view(), name='list_wallet'),




    # path('transaction/add/', views.ListCategoryView.as_view(), name='add_transaction'),
    # path('transaction/list/', views.ListCategoryView.as_view(), name='list_transaction'),
]