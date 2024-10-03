from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, DECIMAL, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import Base


class SensorFileMetadata(Base):
    __tablename__ = "sensor_file_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(255))

    # Relationship to SensorData (one-to-one)
    sensor_data = relationship(
        "SensorData", backref="sensor_file_metadata", cascade="all, delete", passive_deletes=True
    )

    upload_start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    upload_end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)


class SensorData(Base):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_metadata_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_file_metadata.id", ondelete="CASCADE"))
    latitude: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    longitude: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    generationtime_ms: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    utc_offset_seconds: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    timezone: Mapped[str] = mapped_column(String, default="GMT", nullable=False)
    timezone_abbreviation: Mapped[str] = mapped_column(String, default="GMT", nullable=False)
    elevation: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    # Relationships to sensor data tables
    hourly_units = relationship("SensorHourlyUnits", backref="sensor_data", cascade="all, delete", passive_deletes=True)

    hourly_temperatures = relationship(
        "HourlyTemperature", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_humidities = relationship(
        "HourlyHumidity", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_dew_points = relationship(
        "HourlyDewPoint", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_apparent_temperatures = relationship(
        "HourlyApparentTemperature", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_precipitations = relationship(
        "HourlyPrecipitation", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_rains = relationship("HourlyRain", backref="sensor_data", cascade="all, delete", passive_deletes=True)
    hourly_snowfalls = relationship(
        "HourlySnowfall", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_snow_depths = relationship(
        "HourlySnowDepth", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_pressures_msl = relationship(
        "HourlyPressureMSL", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_surface_pressures = relationship(
        "HourlySurfacePressure", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_cloud_covers = relationship(
        "HourlyCloudCover", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_wind_speeds_100m = relationship(
        "HourlyWindSpeed100m", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )
    hourly_wind_directions_100m = relationship(
        "HourlyWindDirection100m", backref="sensor_data", cascade="all, delete", passive_deletes=True
    )


class SensorHourlyUnits(Base):
    __tablename__ = "sensor_hourly_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
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
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyHumidity(Base):
    __tablename__ = "hourly_humidity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor_data.id"), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyDewPoint(Base):
    __tablename__ = "hourly_dew_point"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyApparentTemperature(Base):
    __tablename__ = "hourly_apparent_temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyPrecipitation(Base):
    __tablename__ = "hourly_precipitation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyRain(Base):
    __tablename__ = "hourly_rain"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlySnowfall(Base):
    __tablename__ = "hourly_snowfall"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlySnowDepth(Base):
    __tablename__ = "hourly_snow_depth"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyPressureMSL(Base):
    __tablename__ = "hourly_pressure_msl"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlySurfacePressure(Base):
    __tablename__ = "hourly_surface_pressure"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyCloudCover(Base):
    __tablename__ = "hourly_cloud_cover"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyWindSpeed100m(Base):
    __tablename__ = "hourly_wind_speed_100m"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)


class HourlyWindDirection100m(Base):
    __tablename__ = "hourly_wind_direction_100m"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_data_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sensor_data.id", ondelete="CASCADE"), nullable=False
    )
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)
