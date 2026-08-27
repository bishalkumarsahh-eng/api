import re
import httpx
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .config import settings
from .security import verify
from .limiter import limit

app = FastAPI(title="ElevenYTS Universal Provider API", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.allowed_origins.split(",")],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def normalize_identifier(value: str) -> str:
    value = value.strip()
    if not value or len(value) > 2048:
        raise HTTPException(status_code=400, detail="Invalid media identifier")

    patterns = [
        r"[?&]v=([A-Za-z0-9_-]{3,})",
        r"youtu\.be/([A-Za-z0-9_-]{3,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return value

@app.get("/")
async def root():
    return {
        "success": True,
        "name": "ElevenYTS Universal Provider API",
        "version": "4.0.0",
    }

@app.get("/health")
async def health():
    return {"success": True, "status": "ok"}

@app.get("/status")
async def status():
    return {
        "success": True,
        "status": "online",
        "provider_configured": bool(settings.upstream_download_url),
        "provider_url_configured": bool(settings.upstream_download_url),
    }

@app.get("/download")
async def download(
    url: str = Query(...),
    type: str = Query("audio", pattern="^(audio|video)$"),
    _: None = Depends(verify),
    __: None = Depends(limit),
):
    if not settings.upstream_download_url:
        raise HTTPException(
            status_code=503,
            detail="No authorized upstream provider configured. Set UPSTREAM_DOWNLOAD_URL.",
        )

    identifier = normalize_identifier(url)
    params = {"url": identifier, "type": type}
    headers = {}
    if settings.upstream_api_key:
        headers["X-API-Key"] = settings.upstream_api_key

    timeout = httpx.Timeout(settings.upstream_timeout_seconds, connect=20.0)

    async def stream_upstream():
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            async with client.stream(
                "GET",
                settings.upstream_download_url,
                params=params,
                headers=headers,
            ) as response:
                if response.status_code != 200:
                    body = await response.aread()
                    raise HTTPException(
                        status_code=502,
                        detail=f"Upstream provider returned {response.status_code}: {body[:200].decode(errors='ignore')}",
                    )
                async for chunk in response.aiter_bytes(chunk_size=65536):
                    yield chunk

    # Content type cannot reliably be known before opening the upstream stream.
    # The ElevenYTS client saves the binary response directly using the requested extension.
    media_type = "video/mp4" if type == "video" else "audio/mpeg"
    return StreamingResponse(
        stream_upstream(),
        media_type=media_type,
        headers={"Cache-Control": "no-store"},
    )

@app.get("/provider-check")
async def provider_check(_: None = Depends(verify)):
    if not settings.upstream_download_url:
        return {"success": False, "configured": False}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(settings.upstream_download_url)
        return {
            "success": True,
            "configured": True,
            "reachable": response.status_code < 500,
            "upstream_status": response.status_code,
        }
    except Exception as exc:
        return {"success": False, "configured": True, "reachable": False, "error": str(exc)}
