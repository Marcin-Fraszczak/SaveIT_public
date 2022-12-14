from django.urls import path
from . import views

app_name = 'wallets'

urlpatterns = [
    path('add/', views.AddWalletView.as_view(), name='add_wallet'),
    path('list/', views.ListWalletView.as_view(), name='list_wallet'),
    path('modify/<int:pk>/', views.ModifyWalletView.as_view(), name='modify_wallet'),
    # path('delete/<int:pk>/', views.DeleteWalletView.as_view(), name='delete_wallet'),

    path('transfer/<int:from_pk>/<int:to_pk>/', views.TransferWalletView.as_view(), name='transfer_wallet'),
    path('default/<int:from_pk>/<int:to_pk>/', views.MakeDefaultWalletView.as_view(), name='make_default_wallet'),
]

