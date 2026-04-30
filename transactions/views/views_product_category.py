from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from transactions.models import ProductCategory
from transactions.serializers.serializers_product_category import ProductCategorySerializer
from core.authentication import CookieJWTAuthentication
from globalparameters import globalparameters   

# Product Category Views
class ProductCategoryCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product Category created successfully",
                globalparameters.RESULT_DATA: serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Failed to create Product Category",
            globalparameters.RESULT_DATA: serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductCategoryListAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = ProductCategory.objects.filter(user=request.user).order_by('name')
        serializer = ProductCategorySerializer(categories, many=True)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Product Categories retrieved successfully",
            globalparameters.RESULT_DATA: serializer.data
        }, status=status.HTTP_200_OK)

class ProductCategoryDetailAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return ProductCategory.objects.get(reference_id=pk, user=user)
        except ProductCategory.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk, request.user)
        if not category:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product Category not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCategorySerializer(category)
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Product Category details retrieved successfully",
            globalparameters.RESULT_DATA: serializer.data
        }, status=status.HTTP_200_OK)

class ProductCategoryUpdateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return ProductCategory.objects.get(reference_id=pk, user=user)
        except ProductCategory.DoesNotExist:
            return None

    def patch(self, request, pk):
        category = self.get_object(pk, request.user)
        if not category:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product Category not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product Category updated successfully",
                globalparameters.RESULT_DATA: serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCategoryDeleteAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return ProductCategory.objects.get(reference_id=pk, user=user)
        except ProductCategory.DoesNotExist:
            return None

    def delete(self, request, pk):
        category = self.get_object(pk, request.user)
        if not category:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Product Category not found"
            }, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Product Category deleted successfully"
        }, status=status.HTTP_200_OK)