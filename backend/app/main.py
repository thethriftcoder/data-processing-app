from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.routers import sensor
from app.config.config import CORS_ALLOWED_ORIGINS


app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(sensor.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck():
    """Check application's health."""

    return {"status": "ok"}
