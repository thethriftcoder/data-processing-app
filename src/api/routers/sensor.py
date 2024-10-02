from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.config import config
from src.api.models.base import get_session
from src.api.services import sensor as service


router = APIRouter(prefix="/sensor")


@router.post("/data")
async def save_sensor_data(sensor_data_file: UploadFile, session: AsyncSession = Depends(get_session)):
    """Upload sensor data metrics to the application."""

    if not sensor_data_file.size or sensor_data_file.content_type != "application/json":
        raise HTTPException(422, "Invalid input. Please upload a valid sensor_data JSON file.")

    if sensor_data_file.size > config.MAX_SENSOR_FILE_SIZE:
        raise HTTPException(422, "Invalid input. sensor_data file size exceeds 10MB.")

    sensor_data = await service.process_sensor_data(sensor_data_file)

    return {"data": {"sensor_data": sensor_data, "size": sensor_data_file.size}}
