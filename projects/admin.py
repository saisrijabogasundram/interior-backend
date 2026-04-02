from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'status', 'start_date', 'end_date']
    list_filter = ['status']
    search_fields = ['title', 'customer__username']
