
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import random

def generate_otp():
    """Generate 6 digit numeric OTP"""
    return f"{random.randint(100000, 999999)}"


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_verification_email(request, user):
    """Send verification email to user"""
    # Generate token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Build verification URL
    current_site = get_current_site(request)
    verification_url = f"{settings.BACKEND_URL}/api/auth/verify-email/{uid}/{token}/"
    
    # Prepare email context
    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': current_site.name,
    }
    
    # Render email
    html_message = render_to_string('emails/verify_email.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email
    send_mail(
        subject='Verify Your Email Address',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )



def send_password_reset_otp_email(request, user, otp):
    """
    Send password reset OTP email
    """
    subject = "Password Reset OTP"

    context = {
        "user": user,
        "otp": otp,
        "expiry_minutes": 10,
        "support_email": settings.DEFAULT_FROM_EMAIL,
    }

    html_message = render_to_string(
        "emails/password_reset_otp.html",
        context
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )