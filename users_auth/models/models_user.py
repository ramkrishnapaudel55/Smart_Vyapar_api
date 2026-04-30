from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from generic.models import GenericIdEntity, GenericEntity
from django.conf import settings
from datetime import timedelta

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_super_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_super_admin") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)




class User(AbstractUser, GenericIdEntity):
    """
    Custom User model with 2FA, login attempts tracking, and admin roles
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Basic Information
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    
    # Profile Information
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Account Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    
    # Two-Factor Authentication
    two_fa_enabled = models.BooleanField(default=False)
    two_fa_secret = models.CharField(max_length=32, blank=True, null=True)
    two_fa_backup_codes = models.JSONField(default=list, blank=True)
    
    # Login Attempts & Security
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_device = models.CharField(max_length=255, blank=True)
    
    # Password Management
    password_changed_at = models.DateTimeField(null=True, blank=True)
    require_password_change = models.BooleanField(default=False)
    
    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    # Email Verification
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Password Reset
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_token_created_at = models.DateTimeField(null=True, blank=True)

    role = models.ForeignKey('Role', on_delete=models.PROTECT , null=True, blank=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'bas_users'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['is_active', 'is_verified']),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        """Return the user's short name"""
        return self.first_name or self.username
    
    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until:
            if timezone.now() < self.account_locked_until:
                return False
            else:
                # Unlock account if lock period has passed
                self.account_locked_until = None
                self.failed_login_attempts = 0
                self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
                return False
        return False
    
    def increment_failed_login(self, max_attempts=2000, lock_duration_minutes=30):
        """Increment failed login attempts and lock account if necessary"""
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        
        if self.failed_login_attempts >= max_attempts:
            self.account_locked_until = timezone.now() + timezone.timedelta(minutes=lock_duration_minutes)
        
        self.save(update_fields=['failed_login_attempts', 'last_failed_login', 'account_locked_until'])
    
    def reset_failed_login_attempts(self):
        """Reset failed login attempts after successful login"""
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.account_locked_until = None
        self.save(update_fields=['failed_login_attempts', 'last_failed_login', 'account_locked_until'])
    
    def update_last_activity(self):
        """Update the last activity timestamp"""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])
    
    def has_admin_access(self):
        """Check if user has any admin access"""
        return self.is_admin or self.is_super_admin or self.is_superuser
    
    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.is_super_admin or self.is_superuser
    
    def enable_2fa(self, secret):
        """Enable two-factor authentication"""
        self.two_fa_enabled = True
        self.two_fa_secret = secret
        self.save(update_fields=['two_fa_enabled', 'two_fa_secret'])
    
    def disable_2fa(self):
        """Disable two-factor authentication"""
        self.two_fa_enabled = False
        self.two_fa_secret = None
        self.two_fa_backup_codes = []
        self.save(update_fields=['two_fa_enabled', 'two_fa_secret', 'two_fa_backup_codes'])


class PasswordResetOTP(GenericIdEntity):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False) 
    is_used = models.BooleanField(default=False)
    last_sent_at = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table = "password_reset_otp"

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)



class UserProfile(GenericIdEntity):
    """Extended user profile information"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('zh', 'Chinese'),
        ('hi', 'Hindi'),
        ('ar', 'Arabic'),
    ]
    
    TIMEZONE_CHOICES = [
        ('UTC', 'UTC'),
        ('America/New_York', 'Eastern Time'),
        ('America/Chicago', 'Central Time'),
        ('America/Denver', 'Mountain Time'),
        ('America/Los_Angeles', 'Pacific Time'),
        ('Europe/London', 'London'),
        ('Europe/Paris', 'Paris'),
        ('Asia/Tokyo', 'Tokyo'),
        ('Asia/Kolkata', 'India'),
        ('Australia/Sydney', 'Sydney'),
    ]
    
    # One-to-One relationship with User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Personal Information
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Professional Information
    occupation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    # Social Links
    website = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    twitter = models.URLField(max_length=200, blank=True)
    github = models.URLField(max_length=200, blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    
    # Preferences
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')
    theme = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    
    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    
    # Privacy Settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('friends', 'Friends Only'),
            ('private', 'Private')
        ],
        default='public'
    )
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    
    # Additional Info
    about_me = models.TextField(max_length=1000, blank=True)
    skills = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=17, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    
    # Metadata
    profile_completed = models.BooleanField(default=False)
    profile_completion_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bas_users_profile'
        managed = True
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.email}'s Profile"
    
    def calculate_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields_to_check = [
            self.gender, self.address_line1, self.city, self.country,
            self.postal_code, self.occupation, self.about_me,
            self.user.first_name, self.user.last_name, 
            self.user.phone_number, self.user.profile_picture
        ]
        
        filled_fields = sum(1 for field in fields_to_check if field)
        total_fields = len(fields_to_check)
        
        percentage = int((filled_fields / total_fields) * 100)
        self.profile_completion_percentage = percentage
        self.profile_completed = percentage == 100
        self.save(update_fields=['profile_completion_percentage', 'profile_completed'])
        
        return percentage
    
    def get_full_address(self):
        """Return formatted full address"""
        address_parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, address_parts))



class LoginHistory(GenericEntity):
    """Track user login history"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=255, blank=True)
    login_successful = models.BooleanField(default=True)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'bas_login_history'
        managed = True
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'
        ordering = ['-login_time']
        indexes = [
            models.Index(fields=['user', '-login_time']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.login_time}"
    

class RecentActivity(models.Model):
    ACTIVITY_TYPES = (
        ('USER_REGISTERED', 'User Registered'),
        ('PRODUCT_UPDATED', 'Product Updated'),
        ('ORDER_COMPLETED', 'Order Completed'),
        ('CATEGORY_ADDED', 'Category Added'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "recent_activity"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.activity_type} - {self.created_at}"