from django.contrib import admin
from django.urls import path, include
from sbc import views

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.login_view, name='login'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('logout/', views.logout_view, name='logout'),
        path('accounts/', include('django.contrib.auth.urls')),
]