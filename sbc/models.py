from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('purchasing', 'Purchasing'),
        ('inventory', 'Inventory'),
        ('requestion', 'Requestion'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='requestion')
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"PO-{self.order_number}"

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)

    def __str__(self):
        return self.name

class Requisition(models.Model):
    requisition_number = models.CharField(max_length=20, unique=True)
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"REQ-{self.requisition_number}"