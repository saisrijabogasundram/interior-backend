from rest_framework import serializers
from .models import Product, Cart, Order

class ProductSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'image_url']

    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.image and request:
    #         return request.build_absolute_uri(obj.image.url)
    #     return None


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    product_image = serializers.CharField(
        source='product.image_url',
        read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'product_image',
            'quantity',
            'added_at'
        ]
        read_only_fields = ['customer']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['customer', 'total_amount']