from django.urls import path
from . import views

app_name = 'counterparties'

urlpatterns = [
    path('add/', views.AddCounterpartyView.as_view(), name='add_counterparty'),
    path('list/', views.ListCounterpartyView.as_view(), name='list_counterparty'),
    path('modify/<int:pk>/', views.ModifyCounterpartyView.as_view(), name='modify_counterparty'),
    # path('delete/<int:pk>/', views.DeleteCounterpartyView.as_view(), name='delete_counterparty'),
]

