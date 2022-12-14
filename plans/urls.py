from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('add/', views.AddSavingsPlanView.as_view(), name='add_savings_plan'),
    path('list/', views.ListSavingsPlanView.as_view(), name='list_savings_plan'),
    path('modify/<int:pk>/', views.ModifySavingsPlanView.as_view(), name='modify_savings_plan'),
    path('delete/<int:pk>/', views.DeleteSavingsPlanView.as_view(), name='delete_savings_plan'),

    path('default/<int:from_pk>/<int:to_pk>/', views.MakeDefaultPlanView.as_view(), name='make_default_savings_plan'),
]

