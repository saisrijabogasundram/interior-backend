from django.contrib import admin
from .models import Design

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'style', 'budget', 'created_at']
    list_filter = ['category', 'style', 'budget']
    search_fields = ['title', 'description']
