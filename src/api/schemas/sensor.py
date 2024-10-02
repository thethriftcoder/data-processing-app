from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class SensorHourlyUnits(BaseModel):
    """SensorHourlyUnits contains the units of measurements for weather variable values captured every hour."""

    time: str
    temperature_2m: str
    relative_humidity_2m: str
    dew_point_2m: str
    apparent_temperature: str
    precipitation: str
    rain: str
    snowfall: str
    snow_depth: str
    pressure_msl: str
    surface_pressure: str
    cloud_cover: str
    wind_speed_100m: str
    wind_direction_100m: str


class SensorHourlyData(BaseModel):
    """SensorHourlyData holds values for various weather variables recorded every hour."""

    time: list[datetime]
    temperature_2m: list[Decimal | None]
    relative_humidity_2m: list[Decimal | None]
    dew_point_2m: list[Decimal | None]
    apparent_temperature: list[Decimal | None]
    precipitation: list[Decimal | None]
    rain: list[Decimal | None]
    snowfall: list[Decimal | None]
    snow_depth: list[Decimal | None]
    pressure_msl: list[Decimal | None]
    surface_pressure: list[Decimal | None]
    cloud_cover: list[Decimal | None]
    wind_speed_100m: list[Decimal | None]
    wind_direction_100m: list[Decimal | None]


class SensorData(BaseModel):
    """SensorData defines the schema for an uploaded sensor data file."""

    latitude: Decimal
    longitude: Decimal
    generationtime_ms: Decimal
    utc_offset_seconds: Decimal
    timezone: str = "GMT"
    timezone_abbreviation: str = "GMT"
    elevation: Decimal
    hourly_units: SensorHourlyUnits
    hourly: SensorHourlyData
