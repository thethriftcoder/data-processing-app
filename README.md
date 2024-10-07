# data-processing-app

## application demo video

Github does not allow embedding Youtube videos directly, please click on the thumbnail below to open the video on Youtube:

### Data Processing App Demo 05/10/24

[![Click the link to watch the video on Youtube](https://img.youtube.com/vi/QzvqYJLlZ6w/0.jpg)](https://www.youtube.com/watch?v=QzvqYJLlZ6w).

## Architecture

DB schema diagram:
![DB Schema Diagram](db_schema.png)

Application architecture:
![Application Architecture Diagram](architecture.png)

The FastAPI Backend and Celery Worker services are running in a Google Cloud Run application, within Google Cloud Platform.
They both interact with a caching layer hosting using Redis' own hosting service, and a Postgres database instance running on a private VPS.
Vercel hosts a React-based Frontend that interacts with the FastAPI backend. Vercel automatically deploys any code pushed to the GitHub repository.

The backend also supports auto-scaling up to 3 containers to handle bursts of incoming concurrent requests. All HTTP endpoints are secured with basic auth to prevent unathourized use.

## Workflow

![Application Workflow Diagram](workflow.png)

Users can upload a JSON file containing hourly sensor data, through the `/sensor/data` endpoint. Once uploaded, metadata and general sensor data is stored in the Postgres database. Hourly sensor data is enqueued as a task to be processed by the Celery Worker.

The Celery Worker checks the hourly sensor data for anomalies and interacts with the Cache to store any anomalous values.
Users subscribing to the `/sensor/anomalies` WebSocket endpoint receive real-time updates for anomalous values. All WebSocket messages include the file ID, indicating the file which contains the anomalous value.

Users can connect to the application through the React-based Frontend, to see metadata for all uploaded files. They can view a time-plotted graph for a particular file. The graph shows various sensor data values for all available data entrypoints.

## how to setup and run the backend application

1. create virtual environment: `python3.11 -m venv .venv`.
2. activate virtual environment: `source .venv/bin/activate` for unix systems and `.venv\Scripts\activate.bat` for Windows cmd-based systems.
3. install dependencies: `pip install -r ./backend/requirements.txt` on unix and `pip install -r backend\requirements.txt` on windows.
4. cd into `backend` folder and start application through uvicorn server: `uvicorn --app-dir ./backend app.main:app --reload` on unix and `uvicorn --app-dir backend app.main:app -- reload` for windows (optionally remove the `--reload` param).
5. rename `.env.example` in the `backend` directory to `.env` and set appropriate env var values.
6. check whether application is running successfully by pinging healthcheck endpoint: `curl 127.0.0.1:8000`.

## how to acquire json data

I have included an example `small_data.json` in the `backend` folder which contains hourly weather data for Mumbai from 30/09/2024 to 01/10/2024, and was acquired from [this endpoint](https://archive-api.open-meteo.com/v1/archive?latitude=19.0728&longitude=72.8826&start_date=2024-09-30&end_date=2024-10-01&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,wind_speed_100m,wind_direction_100m&daily=weather_code,temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,sunrise,sunset,daylight_duration,sunshine_duration,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration). You can change the `start_date` request parameter to increase the amount of data fetched.

## how to setup and run the frontend application

1. `cd` into `frontend/app` folder
2. run `npm install` command to install dependencies
3. start application by running `npm run dev` and visit `http://localhost:5173`
