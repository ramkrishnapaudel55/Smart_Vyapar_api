from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    print("CUSTOM EXCEPTION HANDLER TRIGGERED")
    response = exception_handler(exc, context)

    # If DRF doesn't handle it, return default
    if response is None:
        return response

    data = response.data

    message = None

    if isinstance(data, dict):

        # Handle non_field_errors first
        if "non_field_errors" in data and isinstance(data["non_field_errors"], list):
            message = data["non_field_errors"][0]

        else:
            # Get first field error
            field, errors = next(iter(data.items()))

            if isinstance(errors, list):
                message = errors[0]
            else:
                message = errors

    # If we extracted a message, override response format
    if message:
        response.data = {
            "message": message
        }

    return response
