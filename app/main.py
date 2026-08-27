import re, logging
from urllib.parse import urlparse
from fastapi import FastAPI, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .security import check_download_key, check_header_key
from .limiter import limit
from .providers.placeholder import PlaceholderProvider

logging.basicConfig(level=logging.INFO)
app=FastAPI(title="ElevenYTS Compatible Music API", version="3.0.0")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.allowed_origins.split(",")],allow_methods=["*"],allow_headers=["*"])
provider=PlaceholderProvider()

def normalize_identifier(value:str)->str:
    value=value.strip()
    if len(value)>2048: raise ValueError("Identifier too long")
    if "youtube.com" in value or "youtu.be" in value:
        patterns=[r"[?&]v=([A-Za-z0-9_-]{3,})",r"youtu\.be/([A-Za-z0-9_-]{3,})"]
        for p in patterns:
            m=re.search(p,value)
            if m:return m.group(1)
    return value

@app.get("/")
async def root():
    return {"success":True,"name":"ElevenYTS Compatible Music API","version":"3.0.0"}

@app.get("/health")
async def health():
    return {"success":True,"status":"ok"}

@app.get("/download")
async def download(
    url:str=Query(...,description="Video ID or supported provider identifier"),
    type:str=Query("audio",pattern="^(audio|video)$"),
    _:None=Depends(check_download_key),
    __:None=Depends(limit),
):
    identifier=normalize_identifier(url)
    asset=await provider.resolve(identifier,type)
    return RedirectResponse(asset.url,status_code=307)

@app.get("/search")
async def search(q:str=Query(...,min_length=1), _:None=Depends(check_header_key), __:None=Depends(limit)):
    return {"success":True,"query":q,"results":[],"message":"Implement search in your authorized provider adapter."}

@app.get("/docs-info")
async def docs_info():
    return {"bot_compatible_download":"/download?url=VIDEO_ID&type=audio&api_key=YOUR_KEY"}
