from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    user_id: str = Field(min_length=1)
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    language: str | None = None


class Place(BaseModel):
    id: str
    name: str


class TextOutput(BaseModel):
    title: str
    story: str
    facts: list[str]


class AudioOutput(BaseModel):
    url: str | None = None
    duration: float | None = Field(default=None, ge=0)


class VisualOutput(BaseModel):
    url: str | None = None


class ResponseMetadata(BaseModel):
    latency_ms: int = Field(ge=0)
    cached: bool = False


class GenerateResponse(BaseModel):
    request_id: str
    place: Place
    text: TextOutput
    audio: AudioOutput
    visual: VisualOutput
    metadata: ResponseMetadata
