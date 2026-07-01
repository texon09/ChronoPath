from typing import Optional, Union
from pydantic import BaseModel, Field

class TextResponse(BaseModel):
    title: str
    story: str = Field(min_length=1)

class PlaceResponse(BaseModel):
    id: str
    name: str

class AudioResponse(BaseModel):
    url: str
    duration: str

class VisualResponse(BaseModel):
    url: str

class MetaResponse(BaseModel):
    latency_ms: str
    cache_hit: str

class GenerateResponse(BaseModel):
    request_id: str
    # Union to remain strictly backward compatible with older clients expecting a string
    place: Union[PlaceResponse, str]
    text: TextResponse
    audio: Optional[AudioResponse] = None
    visual: Optional[VisualResponse] = None
    safe: bool
    meta: Optional[MetaResponse] = None
