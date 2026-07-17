import asyncio
import time
import uuid

from adk.sequential import SequentialRunner
from adk.parallel import ParallelRunner
from adk.agent_adapter import AgentAdapter

from agents.context_agent import ContextAggregator
from agents.delivery_agent import DeliveryAgent
from agents.journey_agent import JourneyAgent
from agents.location_agent import LocationAgent
from agents.media_agent import MediaAgent
from agents.memory_agent import MemoryAgent
from agents.narrative_agent import NarrativeAgent
from agents.profile_agent import ProfileAgent
from agents.safety_agent import SafetyAgent
from core.session import SessionState
from schemas import GenerateResponse, TextResponse


from adk.loop import FeedbackLoop
from agents.reviewer_agent import ReviewerAgent

class SupervisorAgent:
    def __init__(self):
        self.location_agent = LocationAgent()
        self.profile_agent = ProfileAgent()
        self.journey_agent = JourneyAgent()
        self.context_agent = ContextAggregator()
        self.narrative_agent = NarrativeAgent()
        self.reviewer_agent = ReviewerAgent()
        self.safety_agent = SafetyAgent()
        self.delivery_agent = DeliveryAgent()
        self.media_agent = MediaAgent()
        self.memory_agent = MemoryAgent()

        self.root_runner = SequentialRunner([
            ParallelRunner([
                AgentAdapter(self.location_agent),
                AgentAdapter(self.profile_agent),
                AgentAdapter(self.journey_agent),
            ]),
            AgentAdapter(self.context_agent),
            FeedbackLoop(
                AgentAdapter(self.narrative_agent),
                AgentAdapter(self.reviewer_agent),
                max_attempts=3
            ),
            ParallelRunner([
                AgentAdapter(self.safety_agent),
                AgentAdapter(self.delivery_agent),
                AgentAdapter(self.media_agent),
            ]),
            AgentAdapter(self.memory_agent),
        ])

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
        
        # Execute through the adapter
        await self.root_runner.execute(state)

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
        media = state.get("media", {})

        if not story or not story.get("story"):
            raise ValueError("Narrative agent returned an empty story")
            
        latency = (time.perf_counter() - state.get("started_at", time.perf_counter())) * 1000

        from schemas.response import PlaceResponse, AudioResponse, VisualResponse, MetaResponse
        return GenerateResponse(
            request_id=state.get("request_id"),
            place=PlaceResponse(
                id=location.get("place", ""),
                name=location.get("place", "")
            ),
            text=TextResponse(
                title=f"{location.get('place', '')} - {context.get('context', '')}",
                story=story["story"],
            ),
            audio=AudioResponse(url=media.get("audio_url", ""), duration="0:00") if "audio_url" in media else None,
            visual=VisualResponse(url=media.get("visual_url", "")) if "visual_url" in media else None,
            safe=safety.get("approved", True),
            meta=MetaResponse(
                latency_ms=f"{latency:.2f}",
                cache_hit="false"
            )
        )
