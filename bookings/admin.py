from django.contrib import admin
from .models import Designer, Booking

@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience_years', 'rating', 'is_available']
    list_filter = ['is_available', 'specialization']
    search_fields = ['user__username', 'specialization']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'designer', 'booking_date', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['customer__username', 'designer__user__username']
