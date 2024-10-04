from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.models.sensor import SensorData, SensorFileMetadata


# TODO: maybe create a generic function for this process
async def save_file_metadata(file_metadata_record: SensorFileMetadata, session: AsyncSession) -> int:
    """Marks file metadata record to be saved to the database and returns its ID."""

    try:
        session.add(file_metadata_record)
        await session.flush()
    except DBAPIError as exc:
        print(f"error saving sensor file metadata record to DB: {exc}")
        raise

    return file_metadata_record.id


async def save_base_sensor_data(sensor_data_record: SensorData, session: AsyncSession) -> int:
    """Marks sensor data record to be saved to the database and returns its ID."""

    try:
        session.add(sensor_data_record)
        await session.flush()
    except DBAPIError as exc:
        print(f"error saving sensor data record to DB: {exc}")
        raise

    return sensor_data_record.id


async def save_hourly_data(hourly_data_records: list[Base], session: AsyncSession) -> None:
    """Marks hourly data records to be saved to the database."""

    try:
        session.add_all(hourly_data_records)
    except DBAPIError as exc:
        print(f"error saving hourly sensor data records to DB: {exc}")
        raise


async def mark_upload_completion(file_metadata_id: int, session: AsyncSession) -> None:
    """Marks upload completion time for the file metadata record."""

    try:
        await session.execute(
            update(SensorFileMetadata)
            .where(SensorFileMetadata.id == file_metadata_id)
            .values(upload_end_date=datetime.utcnow())
        )
    except DBAPIError as exc:
        print(f"error updating sensor file upload time in DB: {exc}")
        raise


async def get_all_file_metadata(session: AsyncSession) -> Sequence[SensorFileMetadata]:
    """Gets all file metadata records from the database."""

    try:
        result = await session.scalars(select(SensorFileMetadata))
        file_metadata_records = result.all()
    except DBAPIError as exc:
        print(f"error getting all file metadata from DB: {exc}")
        raise

    return file_metadata_records
