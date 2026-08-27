from fastapi import HTTPException, Query
from .config import settings

async def verify(api_key: str | None = Query(default=None)):
    if settings.api_key and api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
