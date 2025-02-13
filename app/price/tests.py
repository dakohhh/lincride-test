from django.test import TestCase
from .services import PriceService
from .enums import TrafficLevel, DemandLevel

class PriceServiceTests(TestCase):

    def setUp(self):
        self.price_service = PriceService()

    def test_calculate_standard_fare(self):
        distance = 5
        traffic_level = TrafficLevel.LOW
        demand_level = DemandLevel.NORMAL
        fare_details = self.price_service.calculate_fare(distance, traffic_level, demand_level)

        # Standard,  no multipliers applied 
        # Base fare + distance fare
        self.assertEqual(fare_details["total_fare"], 7.5)


    def test_high_traffic_pricing(self):
        distance = 8
        traffic_level = TrafficLevel.HIGH
        demand_level = DemandLevel.NORMAL
        current_hour_of_the_day  =  3
        fare_details = self.price_service.calculate_fare(distance, traffic_level, demand_level, current_hour_of_the_day)
    
        # Standard,  no multipliers applied 
        # Base fare + distance fare
        self.assertEqual(fare_details["total_fare"], 15.75)


    def test_surge_pricing(self):
        distance = 12
        traffic_level = TrafficLevel.NORMAL
        demand_level = DemandLevel.PEAK
        current_hour_of_the_day  =  3
        fare_details = self.price_service.calculate_fare(distance, traffic_level, demand_level, current_hour_of_the_day)

        self.assertEqual(fare_details["total_fare"], 31.32)

    
    def test_peak_hour_with_high_traffic(self):
        distance = 7
        traffic_level = TrafficLevel.HIGH
        demand_level = DemandLevel.PEAK
        current_hour_of_the_day  =  19 # Peak  hour
        fare_details = self.price_service.calculate_fare(distance, traffic_level, demand_level, current_hour_of_the_day)

        self.assertEqual(fare_details["total_fare"], 33.35)
 
    
    def test_long_distance_ride(self):
        distance = 20
        traffic_level = TrafficLevel.LOW
        demand_level = DemandLevel.NORMAL
        current_hour_of_the_day  =  2
        fare_details = self.price_service.calculate_fare(distance, traffic_level, demand_level, current_hour_of_the_day)

        self.assertEqual(fare_details["total_fare"], 22.5)
        