import asyncio
import time
import uuid

from agents.context_agent import ContextAggregator
from agents.delivery_agent import DeliveryAgent
from agents.journey_agent import JourneyAgent
from agents.location_agent import LocationAgent
from agents.narrative_agent import NarrativeAgent
from agents.profile_agent import ProfileAgent
from agents.safety_agent import SafetyAgent
from core.session import SessionState
from schemas import GenerateResponse, TextResponse


class SupervisorAgent:
    def __init__(self):
        self.location_agent = LocationAgent()
        self.profile_agent = ProfileAgent()
        self.journey_agent = JourneyAgent()
        self.context_agent = ContextAggregator()
        self.narrative_agent = NarrativeAgent()
        self.safety_agent = SafetyAgent()
        self.delivery_agent = DeliveryAgent()

    async def execute(self, payload):
        started = time.perf_counter()
        normalized = self._normalize_payload(payload)
        state = SessionState(
            {
                "request_id": str(uuid.uuid4()),
                "request": normalized,
                "started_at": started,
            }
        )

        await asyncio.gather(
            self.location_agent.execute(state),
            self.profile_agent.execute(state),
            self.journey_agent.execute(state),
        )

        await self.context_agent.execute(state)
        await self.narrative_agent.execute(state)

        await asyncio.gather(
            self.safety_agent.execute(state),
            self.delivery_agent.execute(state),
        )

        return self._build_response(state)

    def run(self, payload):
        response = asyncio.run(self.execute(payload))
        return response.model_dump()

    def _normalize_payload(self, payload):
        if "user_id" not in payload and "user" in payload:
            payload = {**payload, "user_id": payload["user"]}
        if "lat" not in payload and "latitude" in payload:
            payload = {**payload, "lat": payload["latitude"]}
        if "lng" not in payload and "longitude" in payload:
            payload = {**payload, "lng": payload["longitude"]}

        required = {"user_id", "lat", "lng"}
        missing = sorted(required - payload.keys())
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        return payload

    def _build_response(self, state):
        location = state.get("location")
        context = state.get("context")
        story = state.get("story")
        safety = state.get("safety")

        if not story or not story.get("story"):
            raise ValueError("Narrative agent returned an empty story")

        return GenerateResponse(
            request_id=state.get("request_id"),
            place=location["place"],
            text=TextResponse(
                title=f"{location['place']} - {context['context']}",
                story=story["story"],
            ),
            safe=safety["approved"],
        )
