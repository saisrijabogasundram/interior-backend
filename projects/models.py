from django.db import models
from django.conf import settings
from bookings.models import Booking

class Project(models.Model):
    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_projects'
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='project',
        blank=True,
        null=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    requirements = models.FileField(upload_to='requirements/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"