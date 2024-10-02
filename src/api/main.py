from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.routers import sensor


app = FastAPI(default_response_class=ORJSONResponse)
app.include_router(sensor.router)


@app.get("/")
def healthcheck():
    """Check application's health."""

    return {"status": "ok"}
