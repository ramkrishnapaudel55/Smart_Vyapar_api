from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.authentication import CookieJWTAuthentication
from users_auth.models.models_notification import Notification
from users_auth.serializers.serializers_notification import NotificationSerializer
from globalparameters import globalparameters

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class MarkNotificationReadView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(reference_id=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response(
                {
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Notification marked as read"
            }, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response(
                {
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: "Notification not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )