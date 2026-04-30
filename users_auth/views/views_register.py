from globalparameters import globalparameters
from django.shortcuts import render, redirect
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from datetime import timedelta
from django.db import transaction
from users_auth.serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    UserSerializer, 
    ChangePasswordSerializer, 
    EmailSerializer
)
from users_auth.utils.utils_register import (
    get_tokens_for_user, 
    get_client_ip, 
    send_verification_email
    )
from users_auth.models import User, RecentActivity
import logging

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                username = request.data.get('username')
                email = request.data.get('email')
                password = request.data.get('password')

                user = User.objects.filter(username=username).first()
                if user:
                    return Response({
                        globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                        globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                        globalparameters.RESULT_MESSAGE: "Username already exists"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = User.objects.filter(email=email).first()
                if user:
                    return Response({
                        globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                        globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                        globalparameters.RESULT_MESSAGE: "Email already exists"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                
                user = serializer.save()
                user.is_active = False
                user.save()
                
                send_verification_email(request, user)

                RecentActivity.objects.create(
                    user=user,
                    activity_type='USER_REGISTERED',
                    description='New user registered'
                )


            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Registration successful. Please check your email to verify your account."
            }, status=status.HTTP_201_CREATED)

        except Exception as exc:
            logger.error(str(exc), exc_info=True)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyEmailView(APIView):
    """
    API endpoint to verify email address
    
   """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            # Decode user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.error(str(exc), exc_info=True)
            # return Response({
            #     'error': 'Invalid verification link'
            # }, status=status.HTTP_400_BAD_REQUEST)
            return redirect(f"{settings.FRONTEND_URL}/verify-email?status=invalid")
        
        # Check if token is valid
        if not default_token_generator.check_token(user, token):
            # return Response({
            #     'error': 'Invalid or expired verification link'
            # }, status=status.HTTP_400_BAD_REQUEST)
            return redirect(f"{settings.FRONTEND_URL}/verify-email?status=invalid")
        
        # if not default_token_generator.check_token(user, token):
        #     return render(
        #         request,
        #         "emails/verify_failed.html",
        #         status=400,
        #     )

        # Check if user is already verified
        if user.is_active:
            # return Response({
            #     'message': 'Email already verified'
            # }, status=status.HTTP_200_OK)
            return redirect(f"{settings.FRONTEND_URL}/verify-email?status=already-verified")
        
        # Activate user
        user.is_active = True
        user.email_verified = True
        user.is_verified = True
        user.email_verified_at = timezone.now()
        user.save()
        
        # Generate tokens for automatic login
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        
        # return Response({
        #     'message': 'Email verified successfully',
        # }, status=status.HTTP_200_OK)
        return redirect(f"{settings.FRONTEND_URL}/verify-email?status=success")


class ResendVerificationEmailView(APIView):
    """
    API endpoint to resend verification email
    
    POST /api/auth/resend-verification/
    Body: {
        "email": "user@example.com"
    }
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailSerializer
    
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "If an account with this email exists, a verification email has been sent."
            }, status=status.HTTP_200_OK)
        
        # Check if user is already verified
        if user.is_active:
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Email is already verified"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has recently requested verification (rate limiting)
        if hasattr(user, 'last_verification_email_sent'):
            time_since_last_email = timezone.now() - user.last_verification_email_sent
            if time_since_last_email < timedelta(minutes=5):
                remaining_time = 5 - (time_since_last_email.seconds // 60)
                return Response({
                    globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                    globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                    globalparameters.RESULT_MESSAGE: f'Please wait {remaining_time} minutes before requesting another verification email'
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        try:
            send_verification_email(request, user)
            
            # Update last sent time
            user.last_verification_email_sent = timezone.now()
            user.save()
            
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_SUCCESS_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_SUCCESS_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Verification email sent successfully"
            }, status=status.HTTP_200_OK)
            
        except Exception as exc:
            logger.error(str(exc), exc_info=True)
            return Response({
                globalparameters.RESULT_CODE: globalparameters.RESULT_ERROR_CODE,
                globalparameters.RESULT_DESCRIPTION: globalparameters.RESULT_ERROR_DESCRIPTION,
                globalparameters.RESULT_MESSAGE: "Failed to send verification email"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


