from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from transactions.models import Transaction, Category
from transactions.serializers import TransactionSerializer
from core.authentication import CookieJWTAuthentication
from globalparameters import globalparameters


class TransactionCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        serializer = TransactionSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Transaction added successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Failed to create Transaction",
            globalparameters.RESULT_DATA: serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TransactionListAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        ).order_by('-date')

        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TransactionUpdateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            transaction = Transaction.objects.get(reference_id=pk, user=request.user)
        except Transaction.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Transaction not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(
            transaction,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Transaction updated successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Failed to update Transaction",
            globalparameters.RESULT_DATA: serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
class TransactionDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            transaction = Transaction.objects.select_related('category').get(
                reference_id=pk,
                user=request.user
            )
        except Transaction.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Transaction not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(transaction)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionDeleteAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            transaction = Transaction.objects.get(reference_id=pk, user=request.user)
        except Transaction.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Transaction not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        transaction.delete()

        return Response(
            {
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Transaction deleted successfully"
            },
            status=status.HTTP_200_OK
        )
