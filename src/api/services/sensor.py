import json

from fastapi import UploadFile, HTTPException
from pydantic import ValidationError

from src.api.schemas.sensor import SensorData


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
