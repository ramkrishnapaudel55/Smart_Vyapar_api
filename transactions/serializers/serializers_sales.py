from rest_framework import serializers
from transactions.models import Sales, Product, Customer

class SalesSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        slug_field='reference_id',
        queryset=Customer.objects.all(),
        required=False,
        allow_null=True
    )
    product = serializers.SlugRelatedField(
        slug_field='reference_id',
        queryset=Product.objects.all()
    )
    product_name = serializers.CharField(source='product.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Sales
        fields = [
            'reference_id',
            'customer',
            'customer_name',
            'product',
            'product_name',
            'quantity',
            'total',
            'payment_mode',
            'status',
            'date',
            'image',
            'created_at'
        ]
        read_only_fields = ['reference_id', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
