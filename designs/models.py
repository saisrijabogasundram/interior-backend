from django.db import models

class Design(models.Model):
    CATEGORY_CHOICES = (
        ('living_room', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'),
        ('office', 'Office'),
        ('modular_furniture', 'Modular Furniture'),
        ('lighting_decor', 'Lighting & Decor'),
    )

    STYLE_CHOICES = (
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('minimalist', 'Minimalist'),
        ('bohemian', 'Bohemian'),
        ('industrial', 'Industrial'),
    )

    BUDGET_CHOICES = (
        ('low', 'Low (Under 50k)'),
        ('medium', 'Medium (50k - 2L)'),
        ('high', 'High (Above 2L)'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    style = models.CharField(max_length=50, choices=STYLE_CHOICES)
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
