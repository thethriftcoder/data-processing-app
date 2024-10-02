import asyncio
from datetime import datetime

from sqlalchemy import DECIMAL, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.api.config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class Base(DeclarativeBase):
    pass


class SensorFileMetadata(Base):
    __tablename__ = "sensor_file_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(255))

    # Relationship to SensorData (one-to-one)
    sensor_data = relationship("SensorData", backref="sensor_file_metadata", uselist=False)

    upload_start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    upload_end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)


class SensorData(Base):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_metadata_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_file_metadata.id"))
    latitude: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    longitude: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    generationtime_ms: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    utc_offset_seconds: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    timezone: Mapped[str] = mapped_column(String, default="GMT", nullable=False)
    timezone_abbreviation: Mapped[str] = mapped_column(String, default="GMT", nullable=False)
    elevation: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)

    # Relationships to sensor data tables
    hourly_units = relationship("SensorHourlyUnits", backref="sensor_data")

    hourly_temperatures = relationship("HourlyTemperature", backref="sensor_data")
    hourly_humidities = relationship("HourlyHumidity", backref="sensor_data")
    hourly_dew_points = relationship("HourlyDewPoint", backref="sensor_data")
    hourly_apparent_temperatures = relationship("HourlyApparentTemperature", backref="sensor_data")
    hourly_precipitations = relationship("HourlyPrecipitation", backref="sensor_data")
    hourly_rains = relationship("HourlyRain", backref="sensor_data")
    hourly_snowfalls = relationship("HourlySnowfall", backref="sensor_data")
    hourly_snow_depths = relationship("HourlySnowDepth", backref="sensor_data")
    hourly_pressures_msl = relationship("HourlyPressureMSL", backref="sensor_data")
    hourly_surface_pressures = relationship("HourlySurfacePressure", backref="sensor_data")
    hourly_cloud_covers = relationship("HourlyCloudCover", backref="sensor_data")
    hourly_wind_speeds_100m = relationship("HourlyWindSpeed100m", backref="sensor_data")
    hourly_wind_directions_100m = relationship("HourlyWindDirection100m", backref="sensor_data")


class SensorHourlyUnits(Base):
    __tablename__ = "sensor_hourly_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[str] = mapped_column(String, nullable=False)
    temperature_2m: Mapped[str] = mapped_column(String, nullable=False)
    relative_humidity_2m: Mapped[str] = mapped_column(String, nullable=False)
    dew_point_2m: Mapped[str] = mapped_column(String, nullable=False)
    apparent_temperature: Mapped[str] = mapped_column(String, nullable=False)
    precipitation: Mapped[str] = mapped_column(String, nullable=False)
    rain: Mapped[str] = mapped_column(String, nullable=False)
    snowfall: Mapped[str] = mapped_column(String, nullable=False)
    snow_depth: Mapped[str] = mapped_column(String, nullable=False)
    pressure_msl: Mapped[str] = mapped_column(String, nullable=False)
    surface_pressure: Mapped[str] = mapped_column(String, nullable=False)
    cloud_cover: Mapped[str] = mapped_column(String, nullable=False)
    wind_speed_100m: Mapped[str] = mapped_column(String, nullable=False)
    wind_direction_100m: Mapped[str] = mapped_column(String, nullable=False)


class HourlyTemperature(Base):
    __tablename__ = "hourly_temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature_2m: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyHumidity(Base):
    __tablename__ = "hourly_humidity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    relative_humidity_2m: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyDewPoint(Base):
    __tablename__ = "hourly_dew_point"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    dew_point_2m: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyApparentTemperature(Base):
    __tablename__ = "hourly_apparent_temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    apparent_temperature: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyPrecipitation(Base):
    __tablename__ = "hourly_precipitation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    precipitation: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyRain(Base):
    __tablename__ = "hourly_rain"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    rain: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlySnowfall(Base):
    __tablename__ = "hourly_snowfall"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    snowfall: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlySnowDepth(Base):
    __tablename__ = "hourly_snow_depth"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    snow_depth: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyPressureMSL(Base):
    __tablename__ = "hourly_pressure_msl"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pressure_msl: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlySurfacePressure(Base):
    __tablename__ = "hourly_surface_pressure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    surface_pressure: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyCloudCover(Base):
    __tablename__ = "hourly_cloud_cover"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cloud_cover: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyWindSpeed100m(Base):
    __tablename__ = "hourly_wind_speed_100m"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    wind_speed_100m: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


class HourlyWindDirection100m(Base):
    __tablename__ = "hourly_wind_direction_100m"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    wind_direction_100m: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=True)


db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(db_url, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.create_task(create_tables())
