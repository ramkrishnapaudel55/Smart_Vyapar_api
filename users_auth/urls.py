from django.urls import path
from users_auth import views

app_name = 'users_auth'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path("verify-email/<uidb64>/<token>/", views.VerifyEmailView.as_view(), name="verify-email",),
    path("resend-verification/",views.ResendVerificationEmailView.as_view(), name="resend-verification",),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path ('me/', views.AuthCheckView.as_view(), name='current-user'),

    # Password Reset
    # path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot-password/verify-otp/', views.VerifyForgotPasswordOTPView.as_view(), name='forgot-password-verify-otp'),
    path('forgot-password/reset-password/', views.ResetPasswordView.as_view(), name='forgot-password-reset-password'),
    path('forgot-password/resend-otp/', views.ResendForgotPasswordOTPView.as_view(), name='forgot-password-resend-otp'),
    
    # User Profile
    path('profile/', views.UserProfileDetailView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile-update'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    # Notifications
    path('notifications/', views.NotificationListAPIView.as_view(), name='notifications'),
    path('notifications/<pk>/read/', views.MarkNotificationReadView.as_view(), name='mark-notification-read'),
]