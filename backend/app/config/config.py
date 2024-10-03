import os

import dotenv


dotenv.load_dotenv()


# 10 MB
MAX_SENSOR_FILE_SIZE = 1024 * 1024 * 10

DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
