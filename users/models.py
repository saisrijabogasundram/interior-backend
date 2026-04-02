from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('designer', 'Designer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('owner', 'Owner'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    def __str__(self):
        return self.email
    # ── Role helper methods ──
    def is_owner(self):
        return self.role == 'owner'

    def is_admin_member(self):
        return self.role in ['admin', 'owner']

    def is_staff_member(self):
        return self.role in ['staff', 'admin', 'owner']

    def is_designer_member(self):
        return self.role == 'designer'

    def is_customer_member(self):
        return self.role == 'customer'