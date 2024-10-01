from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


app = FastAPI(default_response_class=ORJSONResponse)


@app.get("/")
def healthcheck():
    """Check application's health."""

    return {"status": "ok"}
