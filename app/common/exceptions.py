"""
You should probably add a custom exception handler to your project based on
who consumes your APIs. To learn how to create a custom exception handler,
you can check out the Django Rest Framework documentation at:
https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler
from typing import Any, Optional


class BaseCustomException(APIException):
    """Base custom exception that all other custom exceptions should inherit from"""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail: str = _('A server error occurred.')
    default_code: str = 'error'
    
    def __init__(self, detail: Any = None, code: Optional[str] = None):
        super().__init__(detail, code)
        # Store the original detail message for the main message
        self.message = detail if isinstance(detail, str) else str(self.default_detail)
        
        # Ensure the detail is always a list for consistent error formatting
        if isinstance(detail, str):
            self.detail = [detail]
        elif isinstance(detail, list):
            self.detail = detail
        else:
            self.detail = [str(detail)]


class BadRequestException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad Request')
    default_code = 'bad_request'


class UnauthorizedException(BaseCustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'unauthorized'


class ForbiddenException(BaseCustomException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'forbidden'


class NotFoundException(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Resource not found.')
    default_code = 'not_found'


def custom_exception_handler(exc, context):
    """
    Custom exception handler that maintains consistent response format
    across regular responses and exceptions.
    """
    response = exception_handler(exc, context)
    
    if response is None:
        return None

    error_data = {
        "message": "Error",  # Default error message
        "status_code": response.status_code,
        "data": None,
        "errors": []
    }

    if isinstance(exc, ValidationError):
        # Handle DRF ValidationError specially
        error_data["message"] = "Validation Error"  # Keep a consistent validation error message
        
        # Convert validation errors to list format
        errors = []
        for field, field_errors in response.data.items():
            if isinstance(field_errors, list):
                for error in field_errors:
                    errors.append({field : error})
            else:
                errors.append({field : field_errors})
        error_data["errors"] = errors

    elif isinstance(exc, BaseCustomException):
        # Use the original message for the main message
        error_data["message"] = exc.message
        error_data["errors"] = exc.detail

    elif hasattr(exc, 'detail'):
        detail = exc.detail
        
        # Handle JWT and similar structured errors
        if isinstance(detail, dict) and 'messages' in detail:
            error_data["message"] = "Authentication Failed"
            messages = detail['messages']
            
            if isinstance(messages, list):
                errors = []
                for msg in messages:
                    if isinstance(msg, dict) and 'message' in msg:
                        errors.append(msg['message'])
                    else:
                        errors.append(str(msg))
                error_data["errors"] = errors
            else:
                error_data["errors"] = [str(messages)]
                
        # Handle other DRF exceptions
        elif isinstance(detail, str):
            error_data["message"] = detail
            error_data["errors"] = [detail]
        elif isinstance(detail, (list, dict)):
            # Use the first error as the main message
            first_error = detail[0] if isinstance(detail, list) else str(next(iter(detail.values())))
            error_data["message"] = str(first_error)
            error_data["errors"] = [str(error) for error in detail]
        

    response.data = error_data
    return response
