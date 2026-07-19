from pydantic import BaseModel, Field, model_validator


class GenerateRequest(BaseModel):
    user_id: str = Field(min_length=1)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    lat: float | None = Field(default=None, ge=-90, le=90)
    lng: float | None = Field(default=None, ge=-180, le=180)
    language: str | None = None
    age: int | None = None
    origin: str | None = None
    background: str | None = None
    name: str | None = None

    @model_validator(mode="after")
    def normalize_coordinates(self):
        if self.latitude is None and self.lat is not None:
            self.latitude = self.lat
        if self.longitude is None and self.lng is not None:
            self.longitude = self.lng
        if self.latitude is None or self.longitude is None:
            raise ValueError("latitude and longitude are required")
        return self

    def to_agent_payload(self) -> dict:
        return {
            "user_id": self.user_id,
            "lat": self.latitude,
            "lng": self.longitude,
            "language": self.language,
            "age": self.age,
            "origin": self.origin,
            "background": self.background,
            "name": self.name,
        }
