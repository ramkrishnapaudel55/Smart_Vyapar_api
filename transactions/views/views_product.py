from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from transactions.models import Product
from transactions.serializers.serializers_product import ProductSerializer
from core.authentication import CookieJWTAuthentication
from globalparameters import globalparameters


# Product Views
class ProductCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product created successfully",
                globalparameters.RESULT_DATA: serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Failed to create Product",
            globalparameters.RESULT_DATA: serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductListAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(user=request.user).order_by('-created_at')
        serializer = ProductSerializer(products, many=True)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Products retrieved successfully",
            globalparameters.RESULT_DATA: serializer.data
        }, status=status.HTTP_200_OK)

class ProductRetrieveAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Product.objects.get(reference_id=pk, user=user)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk, request.user)
        if not product:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Product details retrieved successfully",
            globalparameters.RESULT_DATA: serializer.data
        }, status=status.HTTP_200_OK)

class ProductUpdateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Product.objects.get(reference_id=pk, user=user)
        except Product.DoesNotExist:
            return None

    def patch(self, request, pk):
        product = self.get_object(pk, request.user)
        if not product:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product updated successfully",
                globalparameters.RESULT_DATA: serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Failed to update Product",
            globalparameters.RESULT_DATA: serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Product.objects.get(reference_id=pk, user=user)
        except Product.DoesNotExist:
            return None

    def delete(self, request, pk):
        product = self.get_object(pk, request.user)
        if not product:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Product deleted successfully"
        }, status=status.HTTP_200_OK)