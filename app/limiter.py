import time
from collections import defaultdict, deque
from fastapi import Request, HTTPException
from .config import settings

buckets = defaultdict(deque)

async def limit(request: Request):
    client = request.query_params.get("api_key") or (request.client.host if request.client else "unknown")
    now = time.time()
    q = buckets[client]
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    q.append(now)
