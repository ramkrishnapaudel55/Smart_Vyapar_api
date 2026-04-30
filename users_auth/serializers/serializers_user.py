from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users_auth.models.models_user import User, UserProfile
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    class Meta:
        model = UserProfile
        fields = [
            'reference_id', 'gender', 'city', 'country', 'occupation', 
            'company', 'about_me', 'language', 'timezone',
            'profile_completion_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['profile_completion_percentage']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'reference_id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'phone_number', 'bio', 'profile_picture', 'is_active','is_admin', 'is_banned', 'is_verified', 'two_fa_enabled','profile', 'date_joined'
        ]
        
        read_only_fields = [
            'reference_id',
            'is_active',
            'is_verified',
            'two_fa_enabled',
            'date_joined',
            'is_admin',
            'is_banned'
        ]

    
    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None





class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    # password2 = serializers.CharField(
    #     write_only=True, 
    #     required=True,
    #     style={'input_type': 'password'}
    # )
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password'
        ]
    
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    def validate_username(self, value):
        """Validate username uniqueness"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def create(self, validated_data):
        """Create new user"""
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=validated_data['email'],
                    username=validated_data['username'],
                    password=validated_data['password'],
                )
                try:
                    UserProfile.objects.create(user=user)
                except Exception as exc:
                    logger.error(str(exc), exc_info=True)
                    raise

                return user
        except Exception as exc:
            logger.error(str(exc), exc_info=True)
            return Response({
                'message': 'Failed to send verification email.',
                'detail': str(exc)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Must include email and password.")

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        # Check if user is banned
        if getattr(user, "is_banned", False):
            raise serializers.ValidationError(
                "Your account has been banned. Please contact support."
            )

        # Check if account is locked
        if user.is_account_locked():
            raise serializers.ValidationError(
                "Account is temporarily locked due to too many failed login attempts. "
                "Please try again later."
            )

        # Check if account is active
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Authenticate user
        user_instance = User.objects.get(email=email)
        user = authenticate(username=user_instance.username, password=password)

        if not user:
            # Increment failed login attempts
            try:
                user = User.objects.get(email=email)
                user.increment_failed_login()
            except User.DoesNotExist:
                pass

            raise serializers.ValidationError("Invalid email or password.")

        # Reset failed login attempts on success
        user.reset_failed_login_attempts()

        attrs['user'] = user
        return attrs

    def validate_email(self, value):
        return value.lower()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, 
        write_only=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "new_password": "Password fields didn't match."
            })
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class EmailSerializer(serializers.Serializer):
    """Serializer for email input"""
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        return value.lower()
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()


class VerifyOTPForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate_email(self, value):
        return value.lower()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def validate_email(self, value):
        return value.lower()

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'profile_picture', 
            'phone_number', 'bio', 'username'
        ]
    
    def validate_username(self, value):
        """Validate username uniqueness excluding current user"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"message": "A user with this username already exists."})
        return value
