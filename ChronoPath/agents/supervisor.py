from agents.context_agent import ContextAggregator
from agents.delivery_agent import DeliveryAgent
from agents.journey_agent import JourneyAgent
from agents.location_agent import LocationAgent
from agents.narrative_agent import NarrativeAgent
from agents.profile_agent import ProfileAgent
from agents.safety_agent import SafetyAgent
from memory.session import SessionMemory


class SupervisorAgent:
    def __init__(self, memory=None):
        self.location_agent = LocationAgent()
        self.profile_agent = ProfileAgent()
        self.journey_agent = JourneyAgent()
        self.context_agent = ContextAggregator()
        self.narrative_agent = NarrativeAgent()
        self.safety_agent = SafetyAgent()
        self.delivery_agent = DeliveryAgent()
        self.memory = memory or SessionMemory()

    def run(self, payload):
        normalized = self._normalize_payload(payload)

        location = self.location_agent.run(normalized)
        profile = self.profile_agent.run(normalized)
        journey = self.journey_agent.run(normalized)

        context = self.context_agent.run(location, profile, journey)
        narrative = self.narrative_agent.run(context)
        safety = self.safety_agent.run(narrative)

        if not safety["approved"]:
            return {
                "error": "Narrative failed safety validation",
                "safety": safety,
            }

        delivery = self.delivery_agent.run(
            narrative,
            network_quality=normalized.get("network_quality", "good"),
        )

        response = {
            "place": location["place"],
            "confidence": location["confidence"],
            "context": context["context"],
            "story": delivery["story"],
            "facts": narrative["facts"],
            "media": delivery["media"],
            "delivery_mode": delivery["mode"],
        }
        self.memory.store_location_history(normalized["user_id"], response)
        return response

    def _normalize_payload(self, payload):
        if "user_id" not in payload and "user" in payload:
            payload = {**payload, "user_id": payload["user"]}

        required = {"user_id", "lat", "lng"}
        missing = sorted(required - payload.keys())
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        return payload
