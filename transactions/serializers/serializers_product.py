from rest_framework import serializers
from transactions.models import Product, ProductCategory

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='reference_id',
        queryset=ProductCategory.objects.all(),
        required=False,
        allow_null=True
    )
    category_details = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'reference_id',
            'name',
            'model',
            'quantity',
            'cost_price',
            'selling_price',
            'description',
            'category',
            'category_details',
            'image',
            'created_at'
        ]
        read_only_fields = ['reference_id', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

    def validate(self, data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
             return data

        name = data.get('name')
        if name:
             # Check for existing product with same name for this user
             # Exclude current instance if updating
             qs = Product.objects.filter(user=request.user, name__iexact=name)
             if self.instance:
                 qs = qs.exclude(pk=self.instance.pk)
             
             if qs.exists():
                 raise serializers.ValidationError({"message": "Product with this name already exists."})
        
        return data
