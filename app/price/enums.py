from enum import StrEnum

class TrafficLevel(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class DemandLevel(StrEnum):
    NORMAL = "normal"
    PEAK = "peak"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class TimeOfDay(StrEnum):
    OFF_PEAK = "off_peak"
    PEAK = "peak"

    @classmethod
    def values(cls):
        return [member.value for member in cls]