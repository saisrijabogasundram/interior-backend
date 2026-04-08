from rest_framework import serializers
from .models import Designer, Booking


class DesignerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Designer
        fields = [
            'id', 'user', 'username', 'email', 'specialization',
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
            'id', 'customer', 'customer_name',
            'guest_name', 'guest_phone',
            'designer', 'designer_name',
            'visit_date', 'time_slot', 'location',
            'budget_range', 'booking_date',
            'status', 'requirements', 'created_at'
        ]
        read_only_fields = ['customer', 'created_at']

    def validate(self, data):
        # Either a logged-in customer OR guest_name + guest_phone must be provided
        customer = self.context.get('request').user if self.context.get('request') else None
        guest_name = data.get('guest_name')
        guest_phone = data.get('guest_phone')

        if not (customer and customer.is_authenticated) and not (guest_name and guest_phone):
            raise serializers.ValidationError(
                'Please provide your name and phone number to book a site visit.'
            )
        return data