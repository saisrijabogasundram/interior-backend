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

    SPECIALIZATION_CHOICES = (
        ('living_room', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'),
        ('office', 'Office'),
        ('bathroom', 'Bathroom'),
        ('modular', 'Modular Furniture'),
        ('lighting', 'Lighting & Decor'),
        ('full_home', 'Full Home Design'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

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