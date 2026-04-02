from rest_framework import serializers
from .models import Designer, Booking

class DesignerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Designer
        fields = [
            'id','user', 'username', 'email', 'specialization',
            'experience_years', 'portfolio_link', 'bio',
            'rating', 'is_available', 'created_at'
        ]
        read_only_fields = ['user'] 


class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    designer_name = serializers.CharField(source='designer.user.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'customer', 'customer_name', 'designer',
            'designer_name', 'booking_date', 'status',
            'requirements', 'created_at'
        ]
        read_only_fields = ['customer','created_at']