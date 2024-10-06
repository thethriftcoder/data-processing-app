from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator


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

    model_config = ConfigDict(hide_input_in_errors=True)

    @model_validator(mode="after")
    def validate_hourly_data(self) -> Self:
        """Performs basic validation by checking whether all data values contain the same number of datapoints."""

        data_points = len(self.time)
        data_fields = self.model_fields.keys()

        for data_field in data_fields:
            data_values = getattr(self, data_field)
            if len(data_values) != data_points:
                raise ValueError(
                    f"Invalid input. Expected {data_points} datapoints for {data_field} but found {len(data_values)}."
                )

        return self


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

    model_config = ConfigDict(hide_input_in_errors=True)


@dataclass
class AnomalousMessageData:
    """AnomalousMessageData represents an anomalous message event parsed into a structured format."""

    file_metadata_id: int
    data_type: str
    time: str
    value: Decimal
