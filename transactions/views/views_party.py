from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from transactions.serializers import CustomerSerializer, TransactionSerializer
from transactions.models import Customer, Transaction
from core.authentication import CookieJWTAuthentication
from django.db import models
from django.db.models import Sum
from globalparameters import globalparameters


import logging

logger = logging.getLogger(__name__)


class CustomerCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Customer created successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Failed to create customer"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomerListAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = Customer.objects.filter(user=request.user)

        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)


class CustomerUpdateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, reference_id):

        try:
            customer = Customer.objects.get(
                reference_id=reference_id,
                user=request.user
            )
        except Customer.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(
            customer,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Customer updated successfully"
                }
            )

        return Response(
            {
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Failed to update customer"
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomerDetailsAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, reference_id):

        try:
            customer = Customer.objects.get(
                reference_id=reference_id,
                user=request.user
            )
        except Customer.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

     
        transactions = Transaction.objects.select_related(
            'category'
        ).filter(
            customer=customer,
            user=request.user
        ).order_by('-date')

     
        total_income = transactions.filter(
            transaction_type='INCOME'
        ).aggregate(total=Sum('amount'))['total'] or 0

   
        total_expense = transactions.filter(
            transaction_type='EXPENSE'
        ).aggregate(total=Sum('amount'))['total'] or 0

 
        due_balance = total_income - total_expense

        customer_data = CustomerSerializer(customer).data
        transaction_data = TransactionSerializer(transactions, many=True).data

        json_response = {
            "customer": customer_data,
            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "due_balance": due_balance
            },
            "transactions": transaction_data
        }

        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Customer details fetched successfully",
            globalparameters.RESULT_DATA: json_response
        }, status=status.HTTP_200_OK)

class CustomerDeleteAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, reference_id):

        try:
            customer = Customer.objects.get(
                reference_id=reference_id,
                user=request.user
            )
        except Customer.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Customer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        customer.delete()

        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Customer deleted successfully"
        }, status=status.HTTP_200_OK)