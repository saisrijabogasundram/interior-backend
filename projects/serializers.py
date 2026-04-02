from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['customer']