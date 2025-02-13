import pendulum
from pendulum import Timezone
from .enums import TrafficLevel, DemandLevel, TimeOfDay

class PriceService:

    BASE_FARE = 2.5
    PER_KM_RATE = 1.0

    TRAFFIC_MULTIPLIERS = {
        TrafficLevel.LOW: 1.0,
        TrafficLevel.NORMAL: 1.2,
        TrafficLevel.HIGH: 1.5
    }

    DEMAND_MULTIPLIERS = {
        DemandLevel.NORMAL: 1,
        DemandLevel.PEAK: 1.8,
    }

    TIME_MULTIPLIERS = {
        TimeOfDay.OFF_PEAK: 1.0,
        TimeOfDay.PEAK: 1.3
    }

    def calculate_fare(self, distance: float, traffic_level: TrafficLevel, demand_level: DemandLevel, current_hour_of_the_day: int = None) -> float:

        # Calculate base fare
        distance_fare = distance * self.PER_KM_RATE

        # Get multipliers
        traffic_multiplier = self.TRAFFIC_MULTIPLIERS[traffic_level]
        demand_multiplier = self.DEMAND_MULTIPLIERS[demand_level]

        # Get the current time, this is to adjust pricing based on peak hours
        if not current_hour_of_the_day:
            current_hour_of_the_day = pendulum.now(Timezone("Africa/Lagos")).hour
            print(current_hour_of_the_day)

        # Is peak hour from 6PM to 9PM
        is_peak_hour = 18 <= current_hour_of_the_day <= 21
        time_multiplier = self.TIME_MULTIPLIERS[TimeOfDay.PEAK if is_peak_hour else TimeOfDay.OFF_PEAK]

        total_fare = (self.BASE_FARE + distance_fare) * demand_multiplier * traffic_multiplier * time_multiplier

        return {
            "base_fare": self.BASE_FARE,
            "distance_fare": distance_fare,
            "traffic_multiplier": traffic_multiplier,
            "demand_multiplier": demand_multiplier,
            "total_fare": round(total_fare, 2)
        }
            
            
            
            


