from math import radians, sin, cos, sqrt, atan2


HERITAGE_PLACES = [
    {
        "place": "Shaniwar Wada",
        "lat": 18.5196,
        "lng": 73.8553,
        "period": "Peshwa Era",
        "themes": ["Maratha Empire", "Peshwa administration", "fortification"],
        "summary": (
            "Shaniwar Wada was the seat of the Peshwas in Pune and a major "
            "political center of the Maratha Empire in the 18th century."
        ),
    },
    {
        "place": "Aga Khan Palace",
        "lat": 18.5525,
        "lng": 73.9015,
        "period": "Indian Freedom Movement",
        "themes": ["Gandhi", "Quit India Movement", "colonial history"],
        "summary": (
            "Aga Khan Palace is closely tied to India's freedom struggle and "
            "served as a place of internment for Mahatma Gandhi and others."
        ),
    },
]


def _distance_km(lat1, lng1, lat2, lng2):
    radius_km = 6371
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    )
    return radius_km * 2 * atan2(sqrt(a), sqrt(1 - a))


def reverse_geocode(lat, lng):
    return {
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "lat": lat,
        "lng": lng,
    }


def heritage_lookup(lat, lng):
    ranked = sorted(
        HERITAGE_PLACES,
        key=lambda place: _distance_km(lat, lng, place["lat"], place["lng"]),
    )
    nearest = dict(ranked[0])
    nearest["distance_km"] = round(
        _distance_km(lat, lng, nearest["lat"], nearest["lng"]), 3
    )
    return nearest


def confidence_score(distance_km):
    if distance_km <= 0.15:
        return 0.95
    if distance_km <= 0.75:
        return 0.82
    if distance_km <= 2:
        return 0.68
    return 0.4
