import os
import django
import sys
import traceback

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
try:
    django.setup()
except Exception as e:
    print("Failed to setup Django:")
    traceback.print_exc()
    sys.exit(1)

print("Django setup successful.")

# Verify imports
try:
    print("Attempting to import SalesRetrieveAPIView from transactions.views...")
    from transactions.views import SalesRetrieveAPIView
    print("Successfully imported SalesRetrieveAPIView.")
except Exception as e:
    print("Failed to import SalesRetrieveAPIView:")
    traceback.print_exc()

try:
    print("Attempting to import SalesUpdateAPIView from transactions.views...")
    from transactions.views import SalesUpdateAPIView
    print("Successfully imported SalesUpdateAPIView.")
except Exception as e:
    print("Failed to import SalesUpdateAPIView:")
    traceback.print_exc()

try:
    print("Attempting to import SalesDeleteAPIView from transactions.views...")
    from transactions.views import SalesDeleteAPIView
    print("Successfully imported SalesDeleteAPIView.")
except Exception as e:
    print("Failed to import SalesDeleteAPIView:")
    traceback.print_exc()

print("Verification complete.")
