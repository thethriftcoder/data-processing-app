from decimal import Decimal
import json
from typing import Sequence

from fastapi import UploadFile, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
import app.models.sensor as models
import app.repository.sensor as repository
from app.schemas.sensor import SensorData, SensorHourlyData, SensorHourlyUnits


async def process_sensor_data(sensor_data_file: UploadFile) -> SensorData:
    """Processes sensor data file content to prepare it for further use, catching and handling any errors during the
    process."""

    try:
        sensor_data_bytes = await sensor_data_file.read()
        sensor_data_json: dict = json.loads(sensor_data_bytes)
    except Exception as exc:
        print(f"error parsing uploaded sensor data as JSON: {exc}")
        raise

    try:
        sensor_data = SensorData(**sensor_data_json)
    except ValidationError as exc:
        print(f"error validating sensor JSON data: {exc}")
        raise HTTPException(422, "Invalid input. Malformed sensor data values.")

    return sensor_data


async def save_initial_data(
    sensor_data_file: UploadFile, sensor_data: SensorData, session: AsyncSession
) -> tuple[int, int]:
    """Parses and saves file metadata and general sensor data to the database. Returns the file metadata and sensor IDs."""

    file_metadata_record = models.SensorFileMetadata(
        name=sensor_data_file.filename, size=sensor_data_file.size, content_type=sensor_data_file.content_type
    )
    file_metadata_id = await repository.save_file_metadata(file_metadata_record, session)

    sensor_data_record = models.SensorData(file_metadata_id=file_metadata_id)
    for field in SensorData.model_fields:
        if "hourly" in field:
            continue

        sensor_value: str | Decimal = getattr(sensor_data, field)
        setattr(sensor_data_record, field, sensor_value)

    sensor_data_id = await repository.save_base_sensor_data(sensor_data_record, session)

    return (file_metadata_id, sensor_data_id)


async def save_hourly_data(sensor_data: SensorData, sensor_data_id: int, session: AsyncSession) -> None:
    """Prepares hourly data records from available sensor hourly data values and saves them to the database.
    Creates db model instances based on the hourly data field type, during iteration over all fields for
    `SensorHourlyData` class."""

    hourly_data_records: list[Base] = []

    hourly_units = sensor_data.hourly_units
    hourly_data = sensor_data.hourly
    time_data_points = hourly_data.time

    hourly_units_record = models.SensorHourlyUnits()

    for field in SensorHourlyUnits.model_fields:
        hourly_value: str = getattr(hourly_units, field)
        setattr(hourly_units_record, field, hourly_value)

    hourly_units_record.sensor_data_id = sensor_data_id

    for field in SensorHourlyData.model_fields:
        if field == "time":
            continue
        elif field == "temperature_2m":
            model = models.HourlyTemperature
        elif field == "relative_humidity_2m":
            model = models.HourlyHumidity
        elif field == "dew_point_2m":
            model = models.HourlyDewPoint
        elif field == "apparent_temperature":
            model = models.HourlyApparentTemperature
        elif field == "precipitation":
            model = models.HourlyPrecipitation
        elif field == "rain":
            model = models.HourlyRain
        elif field == "snowfall":
            model = models.HourlySnowfall
        elif field == "snow_depth":
            model = models.HourlySnowDepth
        elif field == "pressure_msl":
            model = models.HourlyPressureMSL
        elif field == "surface_pressure":
            model = models.HourlySurfacePressure
        elif field == "cloud_cover":
            model = models.HourlyCloudCover
        elif field == "wind_speed_100m":
            model = models.HourlyWindSpeed100m
        else:
            model = models.HourlyWindDirection100m

        values: list = getattr(hourly_data, field)

        for index, value in enumerate(values):
            time = time_data_points[index]
            model_record = model()

            model_record.sensor_data_id = sensor_data_id
            model_record.time = time
            model_record.value = value

            hourly_data_records.append(model_record)

    hourly_data_records.append(hourly_units_record)

    await repository.save_hourly_data(hourly_data_records, session)


async def mark_upload_completion(file_metadata_id: int, session: AsyncSession) -> None:
    """Marks upload completion time for the file metadata record."""

    await repository.mark_upload_completion(file_metadata_id, session)


async def get_all_file_metadata(session: AsyncSession) -> Sequence[models.SensorFileMetadata]:
    """Gets all file metadata records from the database."""

    file_metadata_records = await repository.get_all_file_metadata(session)

    return file_metadata_records
