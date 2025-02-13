from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response

class CustomResponse(Response):
    """
    A custom response class for Django REST Framework that standardizes API responses
    by including status_code, message, and data in the response body.

    Args:
        message (str): Response message to be included in the response
        data (Any, optional): The response payload. Defaults to None
        status_code (int, optional): HTTP status code. Defaults to HTTP_200_OK
        **kwargs: Additional arguments to pass to the parent Response class
    """

    def __init__(
        self, 
        message: str = "", 
        data=None, 
        status_code: int = status.HTTP_200_OK, 
        **kwargs
    ) -> None:
        response_data = {
            "message": message,
            "data": data,
            "status_code": status_code
        }
        super().__init__(data=response_data, status=status_code, **kwargs)



def custom_response_schema(
    serializer_class: type[serializers.Serializer] | None = None,
    status_code: int = status.HTTP_200_OK,
    is_list_view: bool = False
) -> type[serializers.Serializer]:
    """
    Creates a dynamic response schema with status, message and data fields.
    This should be only used for documentation purposes.
    
    Args:
        serializer_class: Optional serializer class for the data field
        status_code: HTTP status code to use in response
        is_list_view: Boolean indicating if response data is a list
    
    Returns:
        A new Serializer class with the specified fields
    """

    outer_status_code = status_code
    outer_is_list_view = is_list_view
    class ResponseSchema(serializers.Serializer):
        status_code = serializers.IntegerField(default=outer_status_code)
        message = serializers.CharField()
        
        def get_data_field():
            base_field = (
                serializer_class() if serializer_class 
                else serializers.Serializer(required=False, allow_null=True)
            )
            return (
                serializers.ListField(child=base_field) 
                if outer_is_list_view else base_field
            )
        
        data = get_data_field()

    return ResponseSchema