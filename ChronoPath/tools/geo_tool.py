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
    if settings.google_maps_api_key:
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={settings.google_maps_api_key}"
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
        except Exception as e:
            print(f"reverse_geocode error: {e}")
            pass
            
    # If no key or fails, gracefully return unknown but validated
    return GeoResult(
        city="Unknown", state="Unknown", country="Unknown",
        lat=lat, lng=lng, display_name="Unknown Location"
    ).model_dump()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def heritage_lookup(lat: float, lng: float) -> dict:
    if settings.google_maps_api_key:
        try:
            radii = [500, 1500, 3000, 5000]
            async with httpx.AsyncClient(timeout=10.0) as client:
                for radius in radii:
                    url = (
                        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                        f"?location={lat},{lng}&radius={radius}&type=point_of_interest"
                        f"&key={settings.google_maps_api_key}"
                    )
                    resp = await client.get(url)
                    resp.raise_for_status()
                    data = resp.json()
                    if data.get("status") == "OK" and data.get("results"):
                        best_place = None
                        min_dist = float('inf')
                        
                        for place_data in data["results"]:
                            plat = place_data["geometry"]["location"]["lat"]
                            plng = place_data["geometry"]["location"]["lng"]
                            dist = _distance_km(lat, lng, plat, plng)
                            
                            if dist < min_dist:
                                min_dist = dist
                                best_place = place_data
                                
                        if best_place:
                            res = HeritageResult(
                                place=best_place["name"],
                                lat=best_place["geometry"]["location"]["lat"],
                                lng=best_place["geometry"]["location"]["lng"],
                                distance_km=round(min_dist, 3),
                                period="Historical Era", # Fallback since Maps lacks this
                                themes=[t.replace('_', ' ').title() for t in best_place.get("types", [])[:3]],
                                summary=best_place.get("vicinity", "Historical landmark")
                            )
                            return res.model_dump()
        except Exception as e:
            print(f"heritage_lookup error: {e}")
            pass

    # Fallback to prevent crash if no API key or no places found nearby
    rev = await reverse_geocode(lat, lng)
    place_name = rev.get("display_name", "Unknown Location") if rev else "Unknown Location"
    
    return HeritageResult(
        place=place_name, lat=lat, lng=lng,
        distance_km=0.0, period="Modern Era", themes=["General location"], summary="Immediate vicinity"
    ).model_dump()

async def confidence_score(distance_km: float) -> float:
    if distance_km <= 0.15: return 0.95
    if distance_km <= 0.75: return 0.82
    if distance_km <= 2: return 0.68
    return 0.4
