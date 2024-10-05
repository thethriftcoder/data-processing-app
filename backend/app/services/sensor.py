import asyncio
from decimal import Decimal
import json
from typing import Sequence

from fastapi import UploadFile, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.celery import app as celery_client
from app.models.base import Base, AsyncSessionLocal
import app.models.sensor as models
import app.repository.sensor as repository
from app.schemas.sensor import SensorData, SensorHourlyData, SensorHourlyUnits


async def parse_sensor_data(sensor_data_file: UploadFile) -> SensorData:
    """Parses sensor data file content to prepare it for further use, catching and handling any errors during the
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


async def get_associated_sensor_data(file_metadata_id: int, session: AsyncSession) -> models.SensorData | None:
    """Gets all sensor data associated with the given file metadata ID."""

    sensor_data = await repository.get_associated_sensor_data(file_metadata_id, session)

    if sensor_data is None:
        raise HTTPException(404, "Sensor data not found.")

    return sensor_data


async def check_hourly_data(sensor_data: SensorData, sensor_data_id: int):
    """Checks hourly data and gathers any anomalies."""

    # TODO: check anomalous data values from chatgpt and add here
    print("checking hourly data for anomalies", sensor_data_id)


async def _process_sensor_data(sensor_data: SensorData, file_metadata_id: int, sensor_data_id: int):
    """Processes sensor data by checking for and reporting anomalies, and saving it to the database."""

    await check_hourly_data(sensor_data, sensor_data_id)
    print(f"checked hourly data for anomalies for file metadata ID:{file_metadata_id}")

    async with AsyncSessionLocal() as session:
        async with session.begin():
            await save_hourly_data(sensor_data, sensor_data_id, session)
            print(f"saved hourly data for file metadata ID:{file_metadata_id}")

            await mark_upload_completion(file_metadata_id, session)
            print(f"marked upload completion for file metadata ID: {file_metadata_id}")


@celery_client.task()
def process_sensor_data(serialized_sensor_data: str, file_metadata_id: int, sensor_data_id: int):
    """Synchronous wrapper task that calls the actual async function."""

    # parse json data back as pydantic model
    sensor_data = SensorData.model_validate_json(serialized_sensor_data)
    print("processing sensor data for file metadata ID:", file_metadata_id)

    # * get the current running loop; avoid asyncio.run as that can create a new loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_process_sensor_data(sensor_data, file_metadata_id, sensor_data_id))

    print("processed sensor data for file metadata ID:", file_metadata_id)
