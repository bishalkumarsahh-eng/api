from fastapi import HTTPException, Query, Header
from .config import settings

async def check_download_key(api_key: str | None = Query(default=None)):
    if settings.api_key and api_key != settings.api_key:
        raise HTTPException(401, "Invalid API key")

async def check_header_key(x_api_key: str | None = Header(default=None)):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(401, "Invalid API key")
