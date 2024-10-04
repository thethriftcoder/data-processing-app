from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config.config import USER_NAME, USER_PASSWORD


security = HTTPBasic(auto_error=True)


def authenticate_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> None:
    """Validates user's credentials against the pre-set username and password."""

    username = credentials.username
    password = credentials.password

    if username != USER_NAME or password != USER_PASSWORD:
        raise HTTPException(401, "Invalid credentials.")
