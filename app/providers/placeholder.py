from fastapi import HTTPException
from .base import MediaProvider, MediaAsset
class PlaceholderProvider(MediaProvider):
    async def resolve(self, identifier:str, media_type:str)->MediaAsset:
        raise HTTPException(
            status_code=501,
            detail="No authorized media provider configured. Implement a MediaProvider for content you are authorized to access and distribute."
        )
