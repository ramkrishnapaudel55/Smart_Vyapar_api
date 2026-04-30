from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from transactions.models import Category
from transactions.serializers import CategorySerializer
from core.authentication import CookieJWTAuthentication
from globalparameters import globalparameters


class CategoryCreateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Category created successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Failed to create category"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CategoryListAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(user=request.user)

        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryUpdateAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            category = Category.objects.get(reference_id=pk, user=request.user)
        except Category.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Category not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Category updated successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Failed to update category"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CategoryDeleteAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            category = Category.objects.get(reference_id=pk, user=request.user)
        except Category.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Category not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        category.delete()

        return Response(
            {
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Category deleted successfully"
            },
            status=status.HTTP_200_OK
        )
