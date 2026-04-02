from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
class Designer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='designer_profile'
    )
    specialization = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    portfolio_link = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    TIME_SLOT_CHOICES = (
        ('morning', 'Morning (9AM - 12PM)'),
        ('afternoon', 'Afternoon (12PM - 4PM)'),
        ('evening', 'Evening (4PM - 7PM)'),
    )
    BUDGET_CHOICES = (
        ('under_1L', 'Under ₹1 Lakh'),
        ('1L_3L', '₹1 Lakh - ₹3 Lakhs'),
        ('3L_5L', '₹3 Lakhs - ₹5 Lakhs'),
        ('5L_10L', '₹5 Lakhs - ₹10 Lakhs'),
        ('above_10L', 'Above ₹10 Lakhs'),
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_bookings'
    )
    designer = models.ForeignKey(
        Designer,
        on_delete=models.CASCADE,
        related_name='designer_bookings'
    )
    visit_date = models.DateField()
    time_slot = models.CharField(
        max_length=20,
        choices=TIME_SLOT_CHOICES,
        default='morning'
    )
    location = models.TextField(
        help_text='Address for site visit',
        default=''
    )
    budget_range = models.CharField(
        max_length=20,
        choices=BUDGET_CHOICES,
        blank=True,
        null=True
    )
    booking_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} → {self.designer.user.username} ({self.status})"
