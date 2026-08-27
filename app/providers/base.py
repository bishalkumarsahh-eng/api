from abc import ABC, abstractmethod
from dataclasses import dataclass
@dataclass
class MediaAsset:
    url:str
    content_type:str|None=None
    filename:str|None=None
class MediaProvider(ABC):
    @abstractmethod
    async def resolve(self, identifier:str, media_type:str)->MediaAsset:
        raise NotImplementedError
