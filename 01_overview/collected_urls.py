from django.contrib import admin
from django.urls import path, include
from . import views


# Globalne urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('transactions/', include('transactions.urls')),
    path('categories/', include('categories.urls')),
    path('plans/', include('plans.urls')),
]



app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('about/', views.AboutView.as_view(), name='about_view'),
    path('contact/', views.ContactView.as_view(), name='contact_view'),
    path('author/', views.AuthorView.as_view(), name='author_view'),
    path('tools/', views.ToolsView.as_view(), name='tools_view'),
    path('notfound/', views.NotFoundView.as_view(), name='not_found_view'),
]



app_name = 'users'

urlpatterns = [
    path('main/', views.DashboardView.as_view(), name='dashboard_view'),
    path('register/', views.RegistrationView.as_view(), name='registration_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('modify/', views.ModifyUserView.as_view(), name='modify_user_view'),
]



app_name = 'transactions'

urlpatterns = [
    path('create/', views.TransactionCreateView.as_view(), name='transaction_create_view'),
    path('list/', views.TransactionListView.as_view(), name='transaction_list_view'),
    path('modify/<int:pk>/', views.TransactionModifyView.as_view(), name='transaction_modify_view'),
    path('delete/<int:pk>/', views.TransactionRemoveView.as_view(), name='transaction_remove_view'),
]



app_name = 'categories'

urlpatterns = [
    path('create/', views.CategoryCreateView.as_view(), name='category_create_view'),
    path('list/', views.CategoryListView.as_view(), name='category_list_view'),
    path('modify/<int:pk>/', views.CategoryModifyView.as_view(), name='category_modify_view'),
    path('delete/<int:pk>/', views.CategoryRemoveView.as_view(), name='category_remove_view'),
]



app_name = 'wallet'

urlpatterns = [
    path('create/', views.WalletCreateView.as_view(), name='wallet_create_view'),
    path('list/', views.WalletListView.as_view(), name='wallet_list_view'),
    path('modify/<int:pk>/', views.WalletModifyView.as_view(), name='wallet_modify_view'),
    path('delete/<int:pk>/', views.WalletRemoveView.as_view(), name='wallet_remove_view'),
    # path('addtransaction/<int:wallet_pk>/<int:transaction_pk>/',
    #      views.AddTransactionToWalletView.as_view(), name='add_transaction_to_wallet_view'),
    # path('removetransaction/<int:wallet_pk>/<int:transaction_pk>/',
    #      views.RemoveTransactionFromWalletView.as_view(), name='remove_transaction_from_wallet_view'),
]



app_name = 'plans'

urlpatterns = [
    path('create/', views.PlanCreateView.as_view(), name='plan_create_view'),
    path('list/', views.PlanListView.as_view(), name='plan_list_view'),
    path('modify/<int:pk>/', views.PlanModifyView.as_view(), name='plan_modify_view'),
    path('delete/<int:pk>/', views.PlanRemoveView.as_view(), name='plan_remove_view'),
]



app_name = 'counterparty'

urlpatterns = [
    path('create/', views.CounterpartyCreateView.as_view(), name='counterparty_create_view'),
    path('list/', views.CounterpartyListView.as_view(), name='counterparty_list_view'),
    path('modify/<int:pk>/', views.CounterpartyModifyView.as_view(), name='counterparty_modify_view'),
    path('delete/<int:pk>/', views.CounterpartyRemoveView.as_view(), name='counterparty_remove_view'),
]
