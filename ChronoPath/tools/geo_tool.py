import httpx
from math import radians, sin, cos, sqrt, atan2
from pydantic import BaseModel
from tenacity import retry, wait_exponential, stop_after_attempt
from core.config import settings

class GeoResult(BaseModel):
    city: str
    state: str
    country: str
    lat: float
    lng: float
    display_name: str

class HeritageResult(BaseModel):
    place: str
    lat: float
    lng: float
    distance_km: float
    period: str
    themes: list[str]
    summary: str

def _distance_km(lat1, lng1, lat2, lng2):
    radius_km = 6371
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    )
    return radius_km * 2 * atan2(sqrt(a), sqrt(1 - a))

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def reverse_geocode(lat: float, lng: float) -> dict:
    if settings.google_api_key:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={settings.google_api_key}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "OK" and data.get("results"):
                results = data["results"]
                city, state, country = "Unknown", "Unknown", "Unknown"
                for comp in results[0].get("address_components", []):
                    if "locality" in comp["types"]:
                        city = comp["long_name"]
                    if "administrative_area_level_1" in comp["types"]:
                        state = comp["long_name"]
                    if "country" in comp["types"]:
                        country = comp["long_name"]
                
                result = GeoResult(
                    city=city,
                    state=state,
                    country=country,
                    lat=lat,
                    lng=lng,
                    display_name=results[0].get("formatted_address", "")
                )
                return result.model_dump()
            
    # If no key or fails, gracefully return unknown but validated
    return GeoResult(
        city="Unknown", state="Unknown", country="Unknown",
        lat=lat, lng=lng, display_name="Unknown Location"
    ).model_dump()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def heritage_lookup(lat: float, lng: float) -> dict:
    if settings.google_api_key:
        url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={lat},{lng}&radius=5000&type=tourist_attraction"
            f"&keyword=historical&key={settings.google_api_key}"
        )
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "OK" and data.get("results"):
                best = data["results"][0]
                plat = best["geometry"]["location"]["lat"]
                plng = best["geometry"]["location"]["lng"]
                dist = round(_distance_km(lat, lng, plat, plng), 3)
                
                res = HeritageResult(
                    place=best["name"],
                    lat=plat,
                    lng=plng,
                    distance_km=dist,
                    period="Historical Era", # Fallback since Maps lacks this
                    themes=[t.replace('_', ' ').title() for t in best.get("types", [])[:3]],
                    summary=best.get("vicinity", "Historical landmark")
                )
                return res.model_dump()

    # Fallback to prevent crash if no API key
    return HeritageResult(
        place="Unknown Heritage Site", lat=lat, lng=lng,
        distance_km=0.0, period="Unknown", themes=[], summary="Unknown"
    ).model_dump()

async def confidence_score(distance_km: float) -> float:
    if distance_km <= 0.15: return 0.95
    if distance_km <= 0.75: return 0.82
    if distance_km <= 2: return 0.68
    return 0.4
