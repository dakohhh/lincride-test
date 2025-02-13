from rest_framework import serializers
from .enums import TrafficLevel, DemandLevel

class FareCalculatorQuerySerializer(serializers.Serializer):
    distance = serializers.FloatField()
    traffic_level = serializers.ChoiceField(choices=TrafficLevel.values())
    demand_level = serializers.ChoiceField(choices=DemandLevel.values())


    def validate_distance(self, value):
        """
        Validate that the distance is positive
        """
        if value <= 0:
            raise serializers.ValidationError("Distance must be greater than 0")
        return value
    
    
    
