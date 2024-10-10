from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from django.utils import timezone

class License(models.Model):
    LICENSE_STATUS = (
        ('active', 'Active'),
        ('revoked', 'Revoked'),
        ('expired', 'Expired'),
    )
    
    key = models.CharField(max_length=64, unique=True)
    product_name = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=LICENSE_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    last_validation = models.DateTimeField(null=True, blank=True)
    
    def is_valid(self):
        if self.status == 'revoked' or self.expiry_date < timezone.now():
            return False
        return True

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('viewer', 'Viewer'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True,
        help_text="The groups this user belongs to."
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions', 
        blank=True,
        help_text="Specific permissions for this user."
    )

    def is_admin(self):
        return self.role == 'admin'
class LicenseLog(models.Model):
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    validation_time = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)
    message = models.CharField(max_length=255)
