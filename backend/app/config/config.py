import os

import dotenv


dotenv.load_dotenv()


# 10 MB
MAX_SENSOR_FILE_SIZE = 1024 * 1024 * 10

ANOMALOUS_DATA_EXPIRY_TIME = 60 * 60 * 12
ANOMALOUS_DATA_KEY = "anomalies"

DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]

USER_NAME = os.environ["USER_NAME"]
USER_PASSWORD = os.environ["USER_PASSWORD"]

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
REDIS_PORT = os.environ["REDIS_PORT"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173",
    "https://sensordata.vercel.app",
    "sensordata.vercel.app",
]

SENSOR_ANOMALOUS_THRESHOLDS: dict[str, tuple[int, int | float]] = {
    "temperature_2m": (-10, 50),
    "relative_humidity_2m": (35, 85),
    "dew_point_2m": (-15, 20),
    "apparent_temperature": (-15, 20),
    "precipitation": (0, 40),
    "snowfall": (0, 10),
    "snow_depth": (0, 0.1),
    "pressure_msl": (950, 1050),
    "surface_pressure": (980, 1020),
    "cloud_cover": (0, 85),
    "wind_speed_100m": (0, 35),
}
