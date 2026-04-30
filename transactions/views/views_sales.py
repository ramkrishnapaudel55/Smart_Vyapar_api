from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from transactions.models import Sales
from transactions.serializers.serializers_sales import SalesSerializer
from core.authentication import CookieJWTAuthentication


from users_auth.models.models_notification import Notification
from globalparameters import globalparameters


class SalesCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SalesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            sale = serializer.save()
            
            Notification.objects.create(
                user=request.user,
                title="New Sale Added",
                message=f"You successfully added a new sale for {sale.product.name} - Amount: {sale.total}",
                notification_type='SALE_ADDED'
            )
            
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Sale created successfully",
                globalparameters.RESULT_DATA: serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Failed to create Sale",
            globalparameters.RESULT_DATA: serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class SalesListAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sales = Sales.objects.filter(user=request.user).order_by('-date')
        serializer = SalesSerializer(sales, many=True)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Sales history retrieved successfully",
            globalparameters.RESULT_DATA: serializer.data
        }, status=status.HTTP_200_OK)

class SalesRetrieveAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Sales.objects.get(reference_id=pk, user=user)
        except Sales.DoesNotExist:
            return None

    def get(self, request, pk):
        sale = self.get_object(pk, request.user)
        if not sale:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Sale not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = SalesSerializer(sale)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Sale details retrieved successfully",
            globalparameters.RESULT_DATA: serializer.data
        }, status=status.HTTP_200_OK)


class SalesUpdateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Sales.objects.get(reference_id=pk, user=user)
        except Sales.DoesNotExist:
            return None

    def patch(self, request, pk):
        sale = self.get_object(pk, request.user)
        if not sale:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Sale not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = SalesSerializer(sale, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Sale updated successfully",
                globalparameters.RESULT_DATA: serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Failed to update Sale",
            globalparameters.RESULT_DATA: serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class SalesDeleteAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Sales.objects.get(reference_id=pk, user=user)
        except Sales.DoesNotExist:
            return None

    def delete(self, request, pk):
        sale = self.get_object(pk, request.user)
        if not sale:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Sale not found"
            }, status=status.HTTP_404_NOT_FOUND)
        # Maybe restore product quantity? Ignoring for now as per basic requirements.
        sale.delete()
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Sale deleted successfully"
        }, status=status.HTTP_200_OK)