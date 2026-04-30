from users_auth.models.models_user import User
from users_auth.serializers.serializers_user import UserSerializer, UserUpdateSerializer
from core.authentication import CookieJWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core import permissions
from globalparameters import globalparameters


class UserProfileDetailView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request},)
        json_response = {
            globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
            globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
            globalparameters.RESULT_MESSAGE: "Profile fetched successfully",
            globalparameters.RESULT_DATA: serializer.data
        }
        return Response(json_response, status=status.HTTP_200_OK)

    
class UserProfileUpdateView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            context={'request': request},
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Profile updated successfully",
                globalparameters.RESULT_DATA: serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
