from rest_framework import serializers
from .models import Design


class DesignSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()

    class Meta:
        model = Design
        fields = ['id', 'title', 'description', 
                  'category', 'style', 'budget', 'image_url']

    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.image and request:
    #         return request.build_absolute_uri(obj.image.url)
    #     return None