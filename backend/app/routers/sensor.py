from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.models.base import get_session
from app.services import sensor as service
from app.services.sensor import process_sensor_data
from app.utilities.basic_auth import authenticate_user


router = APIRouter(prefix="/sensor", dependencies=[Depends(authenticate_user)])


@router.get("/metadata")
async def get_all_file_metadata(session: AsyncSession = Depends(get_session)):
    """Gets all file metadata records from the database."""

    file_metadata_records = await service.get_all_file_metadata(session)

    return {"data": {"file_metadata_records": file_metadata_records}}


@router.get("/data/{file_metadata_id}")
async def get_associated_sensor_data(file_metadata_id: int, session: AsyncSession = Depends(get_session)):
    """Gets all sensor data, including hourly data, associated with the given file metadata ID."""

    sensor_data = await service.get_associated_sensor_data(file_metadata_id, session)
    return {"data": {"sensor_data": sensor_data}}


@router.post("/data")
async def save_sensor_data(sensor_data_file: UploadFile, session: AsyncSession = Depends(get_session)):
    """Upload sensor data metrics to the application."""

    if not sensor_data_file.size or sensor_data_file.content_type != "application/json":
        raise HTTPException(422, "Invalid input. Please upload a valid sensor_data JSON file.")

    if sensor_data_file.size > config.MAX_SENSOR_FILE_SIZE:
        raise HTTPException(422, "Invalid input. sensor_data file size exceeds 10MB.")

    async with session.begin():
        sensor_data = await service.parse_sensor_data(sensor_data_file)
        file_metadata_id, sensor_data_id = await service.save_initial_data(sensor_data_file, sensor_data, session)

    # * serialize pydantic object into json for celery task
    serialized_sensor_data = sensor_data.model_dump_json()
    process_sensor_data.delay(serialized_sensor_data, file_metadata_id, sensor_data_id)

    return {"data": {"message": "File successfully saved to DB."}}
