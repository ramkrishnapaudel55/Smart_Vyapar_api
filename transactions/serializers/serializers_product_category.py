from rest_framework import serializers
from transactions.models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['reference_id', 'name', 'description', 'created_at']
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
            # Check for existing category with same name for this user
            # Exclude current instance if updating
            qs = ProductCategory.objects.filter(user=request.user, name__iexact=name)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise serializers.ValidationError({"message": "Product category with this name already exists."})
        
        return data
