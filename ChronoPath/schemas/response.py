from pydantic import BaseModel, Field


class TextResponse(BaseModel):
    title: str
    story: str = Field(min_length=1)


class GenerateResponse(BaseModel):
    request_id: str
    place: str
    text: TextResponse
    safe: bool
