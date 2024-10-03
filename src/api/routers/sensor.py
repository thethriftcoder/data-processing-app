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

    async with session.begin():
        sensor_data = await service.process_sensor_data(sensor_data_file)
        file_metadata_id, sensor_data_id = await service.save_initial_data(sensor_data_file, sensor_data, session)

        await service.save_hourly_data(sensor_data, sensor_data_id, session)
        await service.mark_upload_completion(file_metadata_id, session)

    return {"data": {"message": "File successfully saved to DB."}}
