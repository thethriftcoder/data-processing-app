from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.config.config import CORS_ALLOWED_ORIGINS
from app.config.cache import redis_client
from app.models.base import create_tables
from app.routers import sensor


@asynccontextmanager
async def lifespan(_):
    await create_tables()
    await redis_client.ping()
    yield


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)

app.include_router(sensor.router)
app.include_router(sensor.ws_router)

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
