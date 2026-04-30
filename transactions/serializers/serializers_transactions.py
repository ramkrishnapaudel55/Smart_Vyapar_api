from rest_framework import serializers
from transactions.models import Category, Transaction, Customer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['reference_id', 'name', 'category_type']


class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    customer = serializers.SlugRelatedField(
        slug_field='reference_id',
        required=False,
        allow_null=True,
        queryset=Customer.objects.all()
    )

    category_details = CategorySerializer(
        source='category',
        read_only=True
    )
    class Meta:
        model = Transaction
        fields = [
            'reference_id',
            'customer',
            'amount',
            'transaction_type',
            'category',
            'category_details',
            'description',
            'date'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        category_ref = validated_data.pop('category')
        customer = validated_data.pop('customer', None)
        transaction_type = validated_data['transaction_type']

        try:
            category = Category.objects.get(
                reference_id=category_ref,
                user=user
            )
        except Category.DoesNotExist:
            raise serializers.ValidationError({
                "category": "Category not found for this user."
            })

        transaction = Transaction.objects.create(
            user=user,
            category=category,
            customer=customer,
            **validated_data
        )

        return transaction
