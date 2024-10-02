import json
from fastapi import APIRouter, HTTPException, UploadFile
import pydantic

from src.api.config import config
from src.api.schemas import sensor as schema


router = APIRouter(prefix="/sensor")


@router.post("/data")
async def save_sensor_data(sensor_data_file: UploadFile):
    """Upload sensor data metrics to the application."""

    print(
        sensor_data_file,
        sensor_data_file.size,
        sensor_data_file.content_type,
        sensor_data_file.filename,
        sensor_data_file.headers,
    )

    if not sensor_data_file.size or sensor_data_file.content_type != "application/json":
        raise HTTPException(422, "Invalid input. Please upload a valid sensor_data JSON file.")

    if sensor_data_file.size > config.MAX_SENSOR_FILE_SIZE:
        raise HTTPException(422, "Invalid input. sensor_data file size exceeds 10MB.")

    try:
        sensor_data_bytes = await sensor_data_file.read()
        sensor_data_json: dict = json.loads(sensor_data_bytes)
    except Exception as exc:
        print(f"error parsing uploaded sensor data as JSON: {exc}")
        raise

    try:
        sensor_data = schema.SensorData(**sensor_data_json)
    except pydantic.ValidationError as exc:
        print(f"error validating sensor JSON data: {exc}")
        raise HTTPException(400, "Invalid input. Malformed sensor data values.")

    return {"data": {"sensor_data": sensor_data, "size": sensor_data_file.size}}
