# Global Parameters - Constants and Response Messages
ORGANIZATION_NAME = ""
ORGANIZATION_NAME_SHORT = ""
ORGANIZATION_LOGO = ""

# Success Messages
SUCCESS_MESSAGE = "Success"
SUCCESS_CREATED = "Resource created successfully"
SUCCESS_UPDATED = "Resource updated successfully"
SUCCESS_DELETED = "Resource deleted successfully"

# Error Messages
ERROR_INVALID_INPUT = "Invalid input provided"
ERROR_NOT_FOUND = "Resource not found"
ERROR_UNAUTHORIZED = "Unauthorized access"
ERROR_FORBIDDEN = "Access forbidden"
ERROR_SERVER_ERROR = "Internal server error"
ERROR_BAD_REQUEST = "Bad request"

# Validation Messages
VALIDATION_EMAIL_INVALID = "Email is invalid"
VALIDATION_PASSWORD_WEAK = "Password is too weak"
VALIDATION_REQUIRED_FIELD = "This field is required"
VALIDATION_LENGTH_ERROR = "Input length is invalid"
VALIDATION_INVALID_COMBINATION_CREDENTIALS = "Invalid combination of credentials"


# Status Codes
STATUS_SUCCESS = 200
STATUS_CREATED = 201
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404
STATUS_SERVER_ERROR = 500

# Default Values
DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1
DEFAULT_TIMEOUT = 30

# Response Format
RESULT_CODE = 'result_code'
RESULT_DESCRIPTION = 'result_description'
RESULT_MESSAGE = 'result_message'
RESULT_DATA = 'results'

# Error Response Format
RESULT_ERROR_CODE = '-100'
RESULT_ERROR_MESSAGE = ''
RESULT_ERROR_DESCRIPTION = 'Error while performing operation'

# Success Response Format
RESULT_SUCCESS_CODE = '100'
RESULT_SUCCESS_MESSAGE = ''
RESULT_SUCCESS_DESCRIPTION = 'Operation performed successfully'


# ----------------------------------------------------------------------------------
# Result Success Status Code
# ----------------------------------------------------------------------------------
RESULT_CODE_SUCCESS = "SUCCESS"
RESULT_CODE_VALIDATION_ERROR = "VALIDATION_ERROR"
RESULT_CODE_AUTH_ERROR = "AUTH_ERROR"
RESULT_CODE_SERVER_ERROR = "SERVER_ERROR"

# ----------------------------------------------------------------------------------
# Result Error Status Code
# ----------------------------------------------------------------------------------
RESULT_CODE_ERROR = "ERROR"


# ----------------------------------------------------------------------------------
# Message
# ----------------------------------------------------------------------------------
MESSAGE = "message"

# ----------------------------------------------------------------------------------
# Response Messages
# ----------------------------------------------------------------------------------
VERIFICATION_EMAIL_SUCCESS = "Verification email sent successfully"
VERIFICATION_EMAIL_ERROR = "Failed to send verification email"
VERIFICATION_EMAIL_ALREADY_VERIFIED = "Email already verified"
VERIFICATION_EMAIL_INVALID_LINK = "Invalid verification link"
VERIFICATION_EMAIL_EXPIRED_LINK = "Verification link expired"
VERIFICATION_EMAIL_ALREADY_VERIFIED = "Email already verified"
VERIFICATION_EMAIL_SUCCESS = "Email verified successfully"

REGISTRATION_ERROR = "Registration failed. Something went wrong while registering your account."
REGISTRATION_SUCCESS = "Registration successful. Please check your email to verify your account."
LOGIN_ERROR = "Login failed. Invalid credentials or inactive account."
LOGIN_SUCCESS = "Login successful."
LOGOUT_ERROR = "Logout failed. Error while logging out."
LOGOUT_SUCCESS = "Logout successful. You have been logged out."
CHANGE_PASSWORD_ERROR = "Password change failed. Error while changing password."
CHANGE_PASSWORD_SUCCESS = "Password changed successfully. Your password has been updated."
RESEND_VERIFICATION_EMAIL_ERROR = "Resend verification email failed. Error while resending verification email."
RESEND_VERIFICATION_EMAIL_SUCCESS = "Resend verification email success. Verification email sent successfully."
VERIFY_EMAIL_ERROR = "Verify email failed. Error while verifying email."
VERIFY_EMAIL_SUCCESS = "Verify email success. Email verified successfully."












