from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializers import FareCalculatorQuerySerializer
from .enums import TrafficLevel, DemandLevel
from .services import PriceService

class FareCalculatorView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Calculate fare",
        tags=["Price"],
        parameters=[
            OpenApiParameter(name="traffic_level", description="Traffic level", required=True, type=OpenApiTypes.STR, enum=TrafficLevel.values()),
            OpenApiParameter(name="demand_level", description="Demand level", required=True, type=OpenApiTypes.STR, enum=DemandLevel.values()),
            OpenApiParameter(name="distance", description="Distance in kilometers", required=True, type=OpenApiTypes.FLOAT),

        ]
    )
    def get(self, request: Request):

        serializer = FareCalculatorQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        distance = serializer.validated_data["distance"]
        traffic_level = serializer.validated_data["traffic_level"]
        demand_level = serializer.validated_data["demand_level"]

        price_service = PriceService()

        fare_details = price_service.calculate_fare(distance, traffic_level, demand_level)

        return Response(fare_details)
        
    