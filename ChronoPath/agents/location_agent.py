from tools.geo_tool import confidence_score, heritage_lookup, reverse_geocode
from tools.history_tool import fetch_history


class LocationAgent:
    async def execute(self, state):
        request = state.get("request")
        location = await self.run(request)
        state.set("location", location)
        return state

    async def run(self, payload):
        lat = payload["lat"]
        lng = payload["lng"]
        geo = await reverse_geocode(lat, lng)
        heritage = await heritage_lookup(lat, lng)
        history = await fetch_history(heritage["place"])
        conf = await confidence_score(heritage["distance_km"])

        return {
            "place": heritage["place"],
            "confidence": conf,
            "distance_km": heritage["distance_km"],
            "geo": geo,
            "period": heritage["period"],
            "themes": heritage["themes"],
            "summary": heritage["summary"],
            "historical_context": history["context"],
            "facts": history["facts"],
        }

