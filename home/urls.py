from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('about/', views.AboutView.as_view(), name='about_view'),
    # path('contact/', views.ContactView.as_view(), name='contact_view'),
    # path('author/', views.AuthorView.as_view(), name='author_view'),
    # path('tools/', views.ToolsView.as_view(), name='tools_view'),
    # path('notfound/', views.NotFoundView.as_view(), name='not_found_view'),
]