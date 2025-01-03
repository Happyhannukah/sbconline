from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import CustomUser, PurchaseOrder, InventoryItem, Requisition
from sbc import models


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    role = request.user.role
    if role == 'admin':
        return render(request, 'admin/dashboard.html')
    elif role == 'purchasing':
        return render(request, 'purchasing/dashboard.html')
    elif role == 'inventory':
        return render(request, 'inventory/dashboard.html')
    elif role == 'requestion':
        return render(request, 'requestion/dashboard.html')
    else:
        return render(request, 'dashboard.html')

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

@login_required
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_purchase_orders = PurchaseOrder.objects.count()
    total_inventory_items = InventoryItem.objects.count()
    total_requisitions = Requisition.objects.count()
    
    context = {
        'total_users': total_users,
        'total_purchase_orders': total_purchase_orders,
        'total_inventory_items': total_inventory_items,
        'total_requisitions': total_requisitions,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def purchasing_dashboard(request):
    recent_purchase_orders = PurchaseOrder.objects.order_by('-created_at')[:5]
    pending_purchase_orders = PurchaseOrder.objects.filter(status='pending').count()
    
    context = {
        'recent_purchase_orders': recent_purchase_orders,
        'pending_purchase_orders': pending_purchase_orders,
    }
    return render(request, 'purchasing/dashboard.html', context)

@login_required
def inventory_dashboard(request):
    low_stock_items = InventoryItem.objects.filter(quantity__lte=models.F('reorder_level'))
    total_items = InventoryItem.objects.count()
    
    context = {
        'low_stock_items': low_stock_items,
        'total_items': total_items,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def requestion_dashboard(request):
    user_requisitions = Requisition.objects.filter(requested_by=request.user).order_by('-created_at')[:5]
    pending_requisitions = Requisition.objects.filter(requested_by=request.user, status='pending').count()
    
    context = {
        'user_requisitions': user_requisitions,
        'pending_requisitions': pending_requisitions,
    }
    return render(request, 'requestion/dashboard.html', context)