from rest_framework import serializers
from transactions.models import Category, Transaction
from transactions.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    reference_id = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'reference_id',
            'name',
            'phone',
            'address'
        ]
