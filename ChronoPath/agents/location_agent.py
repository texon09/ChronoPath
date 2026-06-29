from tools.geo_tool import confidence_score, heritage_lookup, reverse_geocode
from tools.history_tool import fetch_history


class LocationAgent:
    async def execute(self, state):
        request = state.get("request")
        location = self.run(request)
        state.set("location", location)
        return state

    def run(self, payload):
        lat = payload["lat"]
        lng = payload["lng"]
        geo = reverse_geocode(lat, lng)
        heritage = heritage_lookup(lat, lng)
        history = fetch_history(heritage["place"])

        return {
            "place": heritage["place"],
            "confidence": confidence_score(heritage["distance_km"]),
            "distance_km": heritage["distance_km"],
            "geo": geo,
            "period": heritage["period"],
            "themes": heritage["themes"],
            "summary": heritage["summary"],
            "historical_context": history["context"],
            "facts": history["facts"],
        }
