from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class HealthView(GenericAPIView):
    
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        summary="Health check",
        auth=[],
        tags=["Health"],
        responses={200: {"type": "object", "properties": {"status": {"type": "string"}}}}
    )
    def get(self, request):
        return Response(data={"status": "ok"}, status=status.HTTP_200_OK)