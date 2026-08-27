import time
from collections import defaultdict, deque
from fastapi import Request, HTTPException
from .config import settings
buckets=defaultdict(deque)
async def limit(request:Request):
    key=request.query_params.get("api_key") or request.headers.get("X-API-Key") or request.client.host
    now=time.time(); q=buckets[key]
    while q and now-q[0]>60:q.popleft()
    if len(q)>=settings.rate_limit_per_minute: raise HTTPException(429,"Rate limit exceeded")
    q.append(now)
