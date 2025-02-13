from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.openapi import AutoSchema

class CustomAutoSchema(AutoSchema):
    def get_response_serializers(self, view_method):
        # Get the original response serializers
        response_serializers = super().get_response_serializers(view_method)
        
        # If it's a list view, modify the response schema
        if hasattr(view_method, '_is_list_view'):
            for status_code, response in response_serializers.items():
                if isinstance(response.get('content', {}).get('application/json', {}).get('schema', {}).get('items'), dict):
                    response['content']['application/json']['schema']['items'] = {
                        'type': 'object',
                        'properties': response['content']['application/json']['schema']['items']
                    }
        
        return response_serializers

class CustomSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        return schema