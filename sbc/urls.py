from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_login_view, name='my_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('purchasing-dashboard/', views.purchasing_dashboard, name='purchasing_dashboard'),
    path('inventory-dashboard/', views.inventory_dashboard, name='inventory_dashboard'),
    path('requestion-dashboard/', views.requestion_dashboard, name='requestion_dashboard'),
]